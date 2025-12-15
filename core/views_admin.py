from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.core.paginator import Paginator
from django.shortcuts import render
from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname


@staff_member_required
def translation_overview(request):
    """
    Aggregate all modeltranslation fields across registered models into one paginated view.
    """
    page_number = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 50))

    rows = []
    langs = [code.split("-", 1)[0] for code, _ in settings.LANGUAGES]
    default_lang = (getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", "en") or "en").split("-", 1)[0]

    for model in translator.get_registered_models():
        opts = translator.get_options_for_model(model)
        fields = opts.fields
        for obj in model.objects.all():
            for field in fields:
                row = {
                    "model": model._meta.label,
                    "pk": obj.pk,
                    "repr": str(obj),
                    "field": field,
                    "values": {},
                    "values_list": [],
                    "admin_url": None,
                }
                for lang in langs:
                    loc_field = build_localized_fieldname(field, lang)
                    row["values"][lang] = getattr(obj, loc_field, "")
                # also include the base field as default
                row["values"][default_lang] = row["values"].get(default_lang) or getattr(obj, field, "")
                row["values_list"] = [row["values"].get(lang, "") for lang in langs]

                if admin.site.is_registered(model):
                    info = (model._meta.app_label, model._meta.model_name)
                    row["admin_url"] = f"/admin/{info[0]}/{info[1]}/{obj.pk}/change/"
                rows.append(row)

    paginator = Paginator(rows, per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "langs": langs,
        "per_page": per_page,
    }
    return render(request, "admin/translation_overview.html", context)
