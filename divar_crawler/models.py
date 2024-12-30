from django.db import models

class Cars(models.Model):
    titel = models.CharField(max_length=255)
    price = models.CharField(max_length=255, blank=True, null=True)
    linK = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.titel)