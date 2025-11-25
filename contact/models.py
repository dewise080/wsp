from django.db import models

# # # # # # # # # # # # # # # # # #
    # Contact Model #
# # # # # # # # # # # # # # # # # #
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# # # # # # # # # # # # # # # # # #
    # Subscriber Model #
# # # # # # # # # # # # # # # # # #
class Subscriber(models.Model):
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
# # # # # # # # # # # # # # # # # #
      # Contact Page SEO #
# # # # # # # # # # # # # # # # # #
class contactPageSEO(models.Model):
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return self.meta_title
