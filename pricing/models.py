from django.db import models
from ckeditor.fields import RichTextField

# Pricing Model
class pricingSection(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=200, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    button_text = models.CharField(max_length=300, blank=True, null=True)
    button_url = models.CharField(max_length=1000, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    featured_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    
# Pricing Page SEO Model
class pricingPageSEO(models.Model):
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.meta_title
