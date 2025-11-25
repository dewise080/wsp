from django.shortcuts import render, redirect, get_object_or_404
from contact.models import *
from contact.forms import *
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse

# # # # # # # # # # # # # # # # # #
    # Contact Page Front #
# # # # # # # # # # # # # # # # # #
def contactPageFront(request):
    seo = contactPageSEO.objects.first()

    context = {
        'seo' : seo,
    }
    return render(request, 'front/main/contact.html', context)

# # # # # # # # # # # # # # # # # #
    # Contact Submit #
# # # # # # # # # # # # # # # # # #
def ContactSubmit(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Check if there's a session variable for the last submission time
        last_submission_time_str = request.session.get('last_contact_submission_time')

        if last_submission_time_str:
            # Convert the stored time string back to a datetime object
            last_submission_time = datetime.fromisoformat(last_submission_time_str)

            # Calculate the time difference between the last submission and the current time
            time_difference = timezone.now() - last_submission_time

            # Check if less than five minutes have passed since the last submission
            if time_difference.total_seconds() < 300:  # 300 seconds = 5 minutes
                # Calculate the time left for the next submission
                time_left_seconds = 300 - time_difference.total_seconds()
                minutes_left = int(time_left_seconds / 60)
                seconds_left = int(time_left_seconds % 60)

                return JsonResponse({'status': 'error', 'message': f'You can submit again in {minutes_left} minutes and {seconds_left} seconds.'})

        # Save the current time in the session as a string in ISO 8601 format
        request.session['last_contact_submission_time'] = timezone.now().isoformat()

        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Contact form submitted successfully! We will get back to you soon.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid submit! Try again.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid method or not an AJAX request!'})

# # # # # # # # # # # # # # # # # #
    # Subscriber Submit #
# # # # # # # # # # # # # # # # # #        
def SubscriberSubmit(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email') 
        
        # Check if the email already exists in the database
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists!'})
        
        # Check if there's a session variable for the last submission time
        last_submission_time_str = request.session.get('last_submission_time')
        
        if last_submission_time_str:
            # Convert the stored time string back to a datetime object
            last_submission_time = datetime.fromisoformat(last_submission_time_str)
            
            # Calculate the time difference between the last submission and the current time
            time_difference = timezone.now() - last_submission_time
            
            # Check if less than five minutes have passed since the last submission
            if time_difference.total_seconds() < 300:  # 300 seconds = 5 minutes
                # Calculate the time left for the next submission
                time_left_seconds = 300 - time_difference.total_seconds()
                minutes_left = int(time_left_seconds / 60)
                seconds_left = int(time_left_seconds % 60)
                
                return JsonResponse({'status': 'error', 'message': f'You can submit again in {minutes_left} minutes and {seconds_left} seconds.'})
        
        # Save the current time in the session as a string in ISO 8601 format
        request.session['last_submission_time'] = timezone.now().isoformat()
        
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Subscribed successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method or not an AJAX request!'})

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)