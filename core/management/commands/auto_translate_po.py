import glob
import os

import polib
from django.conf import settings
from django.core.management.base import BaseCommand

from rosetta.translate_utils import TranslationException, translate


class Command(BaseCommand):
    help = (
        "Auto-translate PO files using LibreTranslate (via rosetta.translate_utils.translate). "
        "Only fills missing msgstr values unless --force is used."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--locale",
            action="append",
            help="Locale code(s) to process (e.g., tr). Defaults to all locales under LOCALE_PATHS.",
        )
        parser.add_argument(
            "--domain",
            default="django",
            help="PO domain (default: django).",
        )
        parser.add_argument(
            "--source-lang",
            default=getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", "en"),
            help="Source language code (default: settings.MODELTRANSLATION_DEFAULT_LANGUAGE or en).",
        )
        parser.add_argument(
            "--target-lang",
            default="tr",
            help="Target language code (default: tr).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Translate even if msgstr already has content.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not write changes; just show what would happen.",
        )

    def handle(self, *args, **options):
        locales = options.get("locale") or self._discover_locales()
        domain = options["domain"]
        source_lang = options["source_lang"]
        target_lang = options["target_lang"]
        force = options["force"]
        dry_run = options["dry_run"]

        if not locales:
            self.stdout.write(self.style.WARNING("No locales found to process."))
            return

        # quick connectivity check
        try:
            self.stdout.write(self.style.NOTICE("Checking translation backend connectivity..."))
            translate("ping", from_language=source_lang, to_language=target_lang)
            self.stdout.write(self.style.SUCCESS("Translation backend reachable."))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"Translation backend check failed: {exc}"))
            return

        total_files = 0
        total_entries = 0
        translated_entries = 0

        for locale in locales:
            po_paths = self._find_po_files(locale, domain)
            if not po_paths:
                self.stdout.write(self.style.WARNING(f"{locale}: no {domain}.po files found."))
                continue

            for po_path in po_paths:
                total_files += 1
                self.stdout.write(self.style.NOTICE(f"{locale}: processing {po_path}"))
                po = polib.pofile(po_path)
                file_changed = False
                for entry in po:
                    if entry.obsolete:
                        continue
                    if entry.msgstr and not force:
                        continue
                    if entry.msgid_plural:
                        # skip plural entries for now
                        continue

                    source_text = entry.msgid
                    if not source_text:
                        continue

                    total_entries += 1
                    try:
                        translated = translate(
                            source_text, from_language=source_lang, to_language=target_lang
                        )
                    except TranslationException as exc:
                        self.stderr.write(
                            self.style.ERROR(f"{po_path} '{source_text[:40]}...' error: {exc}")
                        )
                        continue

                    entry.msgstr = translated
                    translated_entries += 1
                    file_changed = True
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{po_path} '{source_text[:40]}...' -> '{translated[:40]}...'"
                        )
                    )

                if file_changed and not dry_run:
                    po.save()
                    self.stdout.write(self.style.SUCCESS(f"Saved {po_path}"))
                elif file_changed:
                    self.stdout.write(self.style.WARNING(f"Dry run: {po_path} not saved"))

        summary = (
            f"Processed {total_files} file(s), touched {total_entries} entries, "
            f"translated {translated_entries}."
        )
        if dry_run:
            summary += " (dry run - no files saved)"
        self.stdout.write(self.style.SUCCESS(summary))

    def _discover_locales(self):
        locales = set()
        for path in getattr(settings, "LOCALE_PATHS", []):
            if not os.path.isdir(path):
                continue
            for loc in os.listdir(path):
                loc_path = os.path.join(path, loc)
                if os.path.isdir(loc_path):
                    locales.add(loc)
        return sorted(locales)

    def _find_po_files(self, locale, domain):
        po_files = []
        for path in getattr(settings, "LOCALE_PATHS", []):
            pattern = os.path.join(path, locale, "LC_MESSAGES", f"{domain}.po")
            po_files.extend(glob.glob(pattern))
        return po_files
