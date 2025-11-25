from django.shortcuts import render, redirect
from marketing.forms import *
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from settings.models import websiteSetting
from django.contrib.auth.decorators import login_required
from twilio.rest import Client

@login_required(login_url='logIn')

def emailMarketing(request):
    if request.method == "POST":
        form = EmailSelectForm(request.POST)

        if form.is_valid():
            try:
                website_settings = websiteSetting.objects.first()
                select_all = form.cleaned_data['select_all']
                selected_subscribers = form.cleaned_data['subscribers']
                email_subject = form.cleaned_data['subject']
                message_content = mark_safe(form.cleaned_data['message'])
                manually_added_emails = form.cleaned_data['manually_added_emails']

                recipients = []

                if select_all:
                    recipients.extend([s.email for s in Subscriber.objects.all()])
                else:
                    recipients.extend([s.email for s in selected_subscribers])

                if manually_added_emails:
                    recipients.extend([email.strip() for email in manually_added_emails.split(',')])

                # Loop through recipients and send individual emails
                for email in recipients:
                    send_mail(
                        email_subject,
                        message_content,
                        f'"{website_settings.name}" <{settings.EMAIL_HOST_USER}>',
                        [email],  # Each email is sent to a single recipient
                        fail_silently=False,
                        html_message=message_content  # Set the HTML content of the email
                    )

                messages.success(request, 'Emails sent successfully!')
            except Exception as e:
                messages.warning(request, f'An error occurred: {e}')

            return redirect('emailMarketing')

    else:
        form = EmailSelectForm()

    context = {
        'title': 'Email Marketing',
        'form': form
    }

    return render(request, 'dashboard/main/marketing/email-marketing.html', context)

# SMS Marketing
@login_required(login_url='logIn')
def smsMarketing(request):
    try:
        settings = websiteSetting.objects.first()
        account_sid = str(settings.twilio_sid)
        auth_token = str(settings.twilio_auth_token)
        from_number = str(settings.twilio_from_number)

        client = Client(account_sid, auth_token)
    except AttributeError:
        messages.error(request, 'Twilio settings are not properly configured.')
        return redirect('smsMarketing')

    if request.method == "POST":
        try:
            numbers = request.POST.get('numbers', '')
            message = request.POST.get('message', '')

            if not numbers or not message:
                messages.warning(request, 'Numbers and message are required')
                return redirect('smsMarketing')

            phone_numbers = numbers.split(',')

            status_list = []

            successful_numbers = []
            failed_numbers = []

            for number in phone_numbers:
                try:
                    message = client.messages.create(
                        to=number.strip(), 
                        from_=from_number,
                        body=message
                    )
                    successful_numbers.append(number)
                except Exception as e:
                    failed_numbers.append(number)

            if successful_numbers:
                messages.success(request, f'SMS sent to {", ".join(successful_numbers)}')

            if failed_numbers:
                messages.warning(request, f'SMS sent failed for {", ".join(failed_numbers)}')
                
        except Exception as e:
            messages.warning(request, f'An error occurred: {e}')

        return redirect('smsMarketing')

    return render(request, 'dashboard/main/marketing/sms-marketing.html')

@login_required(login_url='logIn')
def emailFormator(request):

    context ={
        'title' : 'Email Formator'
    }
    return render(request, 'dashboard/main/marketing/email-formator.html', context)

@login_required(login_url='logIn')
def numberFormator(request):

    context ={
        'title' : 'Number Formator'
    }
    return render(request, 'dashboard/main/marketing/number-formator.html', context)

