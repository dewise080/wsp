from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class customPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = RichTextField()
    
    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = customPage.objects.exclude(pk=self.pk)
        slug = original_slug
        counter = 1

        while queryset.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        self.slug = slug
        
    def __str__(self):
        return self.title
    
