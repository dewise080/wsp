from django.urls import path
from marketing.views import *

urlpatterns = [
    path('admin/marketing/email-marketing/', emailMarketing, name='emailMarketing'),
    path('admin/marketing/email-formator/', emailFormator, name='emailFormator'),
    path('admin/marketing/sms-marketing/', smsMarketing, name='smsMarketing'),
    path('admin/marketing/number-formator/', numberFormator, name='numberFormator'),
]
