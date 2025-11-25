from django.db import models

class primaryMenu(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True, null=True)
    order = models.IntegerField()

    def __str__(self):
        return self.name
    
class subMenu(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True, null=True)
    parent_menu = models.ForeignKey(primaryMenu, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
