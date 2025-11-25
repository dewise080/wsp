from django.db import models
from ckeditor.fields import RichTextField

# # # # # # # # # # # # # # # # # #
   # Terms And Condition Model #
# # # # # # # # # # # # # # # # # #

class Terms(models.Model):
    term_texts = RichTextField(blank=True, null=True)

    def __str__(self):
        return 'Terms And Conditions'
    
# # # # # # # # # # # # # # # # # #
   # Privacy Policy Model #
# # # # # # # # # # # # # # # # # #
class Policy(models.Model):
    policy_texts = RichTextField(blank=True, null=True)

    def __str__(self):
        return 'Privacy Policy'