from django import template
from django.utils.timesince import timesince
import random

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def add_name(field, atrname):
    return field.as_widget(attrs={'name': atrname})

@register.filter
def mul(value, arg):
    return value * arg

# Define a list of classes to choose from
CLASS_CHOICES = ["primary", "danger", "warning", "success"]

@register.filter
def random_class(value):
    # Choose a random class from the list
    return random.choice(CLASS_CHOICES)

@register.filter(name='attr')
def attr(field, attribute):
    attr_name, attr_value = attribute.split('=') 
    attrs = {attr_name: attr_value}
    return field.as_widget(attrs=attrs)