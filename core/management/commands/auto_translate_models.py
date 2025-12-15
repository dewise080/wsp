import operator
from functools import reduce

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname

from rosetta.translate_utils import TranslationException, translate


def short_lang(code: str) -> str:
    return (code or "").split("-", 1)[0].lower()


class Command(BaseCommand):
    help = "Auto-translate modeltranslation fields using LibreTranslate (via rosetta.translate_utils.translate)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-lang",
            default=getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", "en"),
            help="Source language code to read from (default: settings.MODELTRANSLATION_DEFAULT_LANGUAGE).",
        )
        parser.add_argument(
            "--target-lang",
            default="tr",
            help="Target language code to write to (default: tr).",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="Chunk size for queryset iteration.",
        )
        parser.add_argument(
            "--model",
            action="append",
            help="Limit to specific models (can be passed multiple times), e.g., home.sliderSection",
        )
        parser.add_argument(
            "--pks",
            action="append",
            help="Limit to specific primary key(s); can be passed multiple times or comma-separated.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Stop after translating this many objects (across models).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Translate even if the target field already has content.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not write changes; just show what would happen.",
        )

    def handle(self, *args, **options):
        source_lang = short_lang(options["source_lang"])
        target_lang = short_lang(options["target_lang"])
        batch_size = options["batch_size"]
        limit = options.get("limit")
        force = options["force"]
        dry_run = options["dry_run"]
        raw_models = options.get("model")
        if isinstance(raw_models, str):
            model_filters = [raw_models.lower()]
        else:
            model_filters = [m.lower() for m in (raw_models or [])]
        verbosity = int(options.get("verbosity", 1))

        registered_models = translator.get_registered_models()
        if model_filters:
            registered_models = [
                m for m in registered_models if self._matches_filter(m, model_filters)
            ]

        # Debug visibility: show what models are registered and which filters were applied.
        available_labels = [m._meta.label_lower for m in translator.get_registered_models()]
        if verbosity >= 2:
            self.stdout.write(self.style.NOTICE(f"Registered models: {available_labels}"))
        if model_filters and not registered_models:
            self.stdout.write(
                self.style.WARNING(
                    f"Model filters {model_filters} matched none of registered models; available: {available_labels}"
                )
            )

        raw_pks = options.get("pks") or []
        pks = []
        for entry in raw_pks:
            for part in str(entry).split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    pks.append(int(part))
                except ValueError:
                    self.stderr.write(self.style.WARNING(f"Ignoring invalid pk '{part}'"))

        if not registered_models:
            self.stdout.write(self.style.WARNING("No registered models found to translate."))
            return

        # quick connectivity check to the translation backend
        try:
            if verbosity >= 1:
                self.stdout.write(self.style.NOTICE("Checking translation backend connectivity..."))
            _ = translate("ping", from_language=source_lang, to_language=target_lang)
            if verbosity >= 1:
                self.stdout.write(self.style.SUCCESS("Translation backend reachable."))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Translation backend check failed: {exc}"))
            return

        total_saved = 0
        for model in registered_models:
            model_saved = self._translate_model(
                model=model,
                source_lang=source_lang,
                target_lang=target_lang,
                batch_size=batch_size,
                pks=pks,
                limit=limit,
                force=force,
                dry_run=dry_run,
                verbosity=verbosity,
            )
            total_saved += model_saved
            if limit and total_saved >= limit:
                break

        summary = f"Translated {total_saved} object(s) to {target_lang}"
        if dry_run:
            summary += " (dry run - no changes saved)"
        self.stdout.write(self.style.SUCCESS(summary))

    def _matches_filter(self, model, filters):
        label = model._meta.label_lower  # e.g., home.slidersection
        return any(label == f.lower() for f in filters)

    def _translate_model(
        self,
        *,
        model,
        source_lang: str,
        target_lang: str,
        batch_size: int,
        pks: list[int],
        limit: int,
        force: bool,
        dry_run: bool,
        verbosity: int,
    ) -> int:
        opts = translator.get_options_for_model(model)
        fields = opts.fields
        target_fields = {
            field: build_localized_fieldname(field, target_lang) for field in fields
        }
        source_fields = {
            field: build_localized_fieldname(field, source_lang) for field in fields
        }

        model_label = model._meta.label

        q_objects = []
        if not force:
            for target in target_fields.values():
                q_objects.append(Q(**{f"{target}__isnull": True}) | Q(**{target: ""}))
        base_q = reduce(operator.or_, q_objects) if q_objects else Q()

        queryset = model.objects.all()
        if pks:
            queryset = queryset.filter(pk__in=pks)
        if base_q.children:
            queryset = queryset.filter(base_q)

        total = queryset.count()
        if total == 0:
            self.stdout.write(self.style.WARNING(f"{model_label}: nothing to translate."))
            return 0

        if verbosity >= 1:
            self.stdout.write(self.style.NOTICE(f"{model_label}: processing {total} object(s)..."))
        saved_count = 0

        for obj in queryset.iterator(chunk_size=batch_size):
            changed_fields = []
            for field in fields:
                target_field = target_fields[field]
                if not force:
                    current_val = getattr(obj, target_field, None)
                    if current_val:
                        continue

                source_field = source_fields.get(field) or field
                source_value = getattr(obj, source_field, None) or getattr(obj, field, None)
                if not source_value:
                    continue

                try:
                    translated = translate(
                        str(source_value),
                        from_language=source_lang,
                        to_language=target_lang,
                    )
                except TranslationException as exc:
                    self.stderr.write(
                        self.style.ERROR(f"{model_label}#{obj.pk} {field} translation error: {exc}")
                    )
                    continue

                setattr(obj, target_field, translated)
                changed_fields.append(target_field)
                if verbosity >= 1:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{model_label}#{obj.pk} {field}: '{source_value}' -> '{translated}'"
                        )
                    )

            if changed_fields:
                saved_count += 1
                if not dry_run:
                    try:
                        obj.save(update_fields=changed_fields)
                    except Exception as exc:
                        saved_count -= 1  # rollback count since save failed
                        self.stderr.write(
                            self.style.ERROR(
                                f"{model_label}#{obj.pk} save error: {exc} (fields: {changed_fields})"
                            )
                        )

            if limit and saved_count >= limit:
                break

        if verbosity >= 1:
            self.stdout.write(self.style.SUCCESS(f"{model_label}: saved {saved_count} object(s)."))
        return saved_count
