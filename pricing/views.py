from django.shortcuts import render
from pricing.models import *
from blog.models import Blogs

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