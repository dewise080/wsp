from django.db import models

# About Page Model
class aboutPage(models.Model):
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    feature1 = models.CharField(max_length=100, blank=True, null=True)
    
    feature2 = models.CharField(max_length=100, blank=True, null=True)
    
    feature3 = models.CharField(max_length=100, blank=True, null=True)
    
    years_of_experience = models.IntegerField(blank=True, null=True)
    
    image1 = models.ImageField(upload_to='AboutPage/', blank=True, null=True)
    image2 = models.ImageField(upload_to='AboutPage/', blank=True, null=True)
    image3 = models.ImageField(upload_to='AboutPage/', blank=True, null=True)

    def __str__(self):
        return self.title

# Team Section Model
class teamSection(models.Model):
    image = models.ImageField(upload_to='Teams/', blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=500, blank=True, null=True)
    instagram = models.CharField(max_length=500, blank=True, null=True)
    linkedin = models.CharField(max_length=500, blank=True, null=True)
    whatsapp = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
    
class aboutPageSEO(models.Model):
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return self.meta_title