from django.shortcuts import render, get_object_or_404
from service.models import servicePageSEO
from home.models import serviceSection,testimonialsSection
from pricing.models import pricingSection

def serviceFrontPage(request):
    seo = servicePageSEO.objects.first()
    services = serviceSection.objects.all()
    testimonials = testimonialsSection.objects.all()
    pricings = pricingSection.objects.all()

    context ={
        'seo' : seo,
        'services' : services,
        'testimonials' : testimonials,
        'pricings' : pricings,

    }
    return render(request, 'front/main/service.html', context)

def serviceDetail(request, slug):
    service = get_object_or_404(serviceSection, slug=slug)
    services = serviceSection.objects.all()

    context = {
        'service' : service,
        'services' : services,
    }
    return render(request, 'front/main/partial/service-details.html', context)


def error_404(request, exception):
    return render(request, 'error/404.html', status=404)