from django.db import models

class Car(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    year = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True)
    source_url = models.URLField(max_length=500)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.price} ({self.year})"