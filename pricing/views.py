import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pricing.models import *
from blog.models import Blogs
from core.translation_hooks import trigger_auto_translate

def pricingPageFront(request):
    seo = pricingPageSEO.objects.first()
    pricings = pricingSection.objects.all()
    blogs = Blogs.objects.all().order_by('?')

    context = {
        'seo' : seo,
        'pricings' : pricings,
        'blogs' : blogs,
    }
    return render(request, 'front/main/pricing.html', context)

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)

def serialize_pricing(pricing):
    return {
        "id": pricing.id,
        "title": pricing.title,
        "subtitle": pricing.subtitle,
        "price": pricing.price,
        "description": pricing.description,
        "button_text": pricing.button_text,
        "button_url": pricing.button_url,
        "is_featured": pricing.is_featured,
        "featured_text": pricing.featured_text,
    }

def parse_bool(value, default=None):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    val = str(value).lower().strip()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off"):
        return False
    return default

@csrf_exempt
def api_pricings(request):
    """
    CRUD-lite endpoint to power inline editing for pricingSection.
    Supports:
      - GET (list or ?id=)
      - POST (create)
      - PATCH/PUT (partial update by ?id=)
    """
    if request.method == "GET":
        pricing_id = request.GET.get("id")
        if pricing_id:
            try:
                pricing_obj = pricingSection.objects.get(pk=int(pricing_id))
            except (ValueError, pricingSection.DoesNotExist):
                return JsonResponse({"detail": "Pricing not found"}, status=404)
            return JsonResponse(serialize_pricing(pricing_obj), status=200)

        data = [serialize_pricing(p) for p in pricingSection.objects.all()]
        return JsonResponse({"count": len(data), "items": data}, status=200)

    if request.method not in ["POST", "PATCH", "PUT"]:
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    payload = {}
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON payload"}, status=400)
    else:
        payload = request.POST

    if request.method == "POST":
        title = payload.get("title")
        if not title:
            return JsonResponse({"detail": "title is required"}, status=400)

        pricing_obj = pricingSection(
            title=title,
            subtitle=payload.get("subtitle"),
            price=payload.get("price"),
            description=payload.get("description"),
            button_text=payload.get("button_text"),
            button_url=payload.get("button_url"),
            is_featured=parse_bool(payload.get("is_featured"), False),
            featured_text=payload.get("featured_text"),
        )
        pricing_obj.save()
        trigger_auto_translate('pricing.pricingsection', pricing_obj.id)
        return JsonResponse(serialize_pricing(pricing_obj), status=201)

    pricing_id = request.GET.get("id")
    if not pricing_id:
        return JsonResponse({"detail": "id is required for update"}, status=400)
    try:
        pricing_obj = pricingSection.objects.get(pk=int(pricing_id))
    except (ValueError, pricingSection.DoesNotExist):
        return JsonResponse({"detail": "Pricing not found"}, status=404)

    for field in ["title", "subtitle", "price", "description", "button_text", "button_url", "featured_text"]:
        if field in payload:
            setattr(pricing_obj, field, payload.get(field))

    if "is_featured" in payload:
        pricing_obj.is_featured = parse_bool(payload.get("is_featured"), pricing_obj.is_featured)

    pricing_obj.save()
    trigger_auto_translate('pricing.pricingsection', pricing_obj.id)
    return JsonResponse(serialize_pricing(pricing_obj), status=200)
