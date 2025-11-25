from django.shortcuts import render
from legal.models import Terms, Policy

def termsPageFront(request):
    term = Terms.objects.first()

    context = {
        'title' : 'Terms & Conditions',
        'term' : term,
    }
    return render(request, 'front/main/terms.html', context)

def policyPageFront(request):
    policy = Policy.objects.first()

    context = {
        'title' : 'Privacy Policy',
        'policy' : policy,
    }
    return render(request, 'front/main/policy.html', context)

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)