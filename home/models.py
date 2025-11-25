from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Sliders Model
class sliderSection(models.Model):
    image = models.ImageField(upload_to='Home/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    button1_text = models.CharField(max_length=100, blank=True, null=True)
    button1_url = models.CharField(max_length=500, blank=True, null=True)
    button2_text = models.CharField(max_length=100, blank=True, null=True)
    button2_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "1. Slider Section"

# Services Model
class serviceSection(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    fontawesome_icon_class = models.CharField(max_length=100, blank=True, null=True)
    detail_page_image = models.ImageField(upload_to='Services/', blank=True, null=True)
    detail_page_description = RichTextField(blank=True, null=True)
    show_call_now_widget = models.BooleanField(default=True)
        
    def save(self, *args, **kwargs):
        if self.name:
            base_slug = slugify(self.name) or "service"
            slug = base_slug
            queryset = serviceSection.objects.exclude(pk=self.pk)
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "2. Service Section"
        
# About Section Model
class aboutSection(models.Model):
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    ranking_number = models.IntegerField(blank=True, null=True)
    tag_line = models.CharField(max_length=200, blank=True, null=True)
    experience = models.CharField(max_length=200, blank=True, null=True)
    
    image = models.ImageField(upload_to='AboutSection/', blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='AboutSection/', blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "3. About Section"

# Funfacts Section Model
class funFactSection(models.Model):
    fontawesome_icon_class = models.CharField(max_length=200, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    count_after = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "4. Fun Fact Section"

# Project and Project category Section Model
class projectCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.name:
            base_slug = slugify(self.name) or "category"
            slug = base_slug
            queryset = projectCategory.objects.exclude(pk=self.pk)
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class projectSection(models.Model):
    image = models.ImageField(upload_to='Projects/', blank=True, null=True)
    category = models.ForeignKey(projectCategory, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.title:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            queryset = projectSection.objects.exclude(pk=self.pk)
            counter = 1

            while queryset.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)
        
    def getProjectImage(self):
        if self.image:
            return self.image.url
        else:
            return 'https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg'

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "5.Project Section"

# Client Section Model
class clientSection(models.Model):
    client_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='Clients/', blank=True, null=True)

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name_plural = "6.Client Section"

# Testimonials Model
class testimonialsSection(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Testimonials/', blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "7.Testimonial Section"

# Home Page SEO Model
class homePageSEO(models.Model):
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.meta_title
