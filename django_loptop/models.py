from django.db import models

class Loptop(models.Model):
        title = models.CharField(max_length=255)
        price = models.PositiveBigIntegerField()
        brand = models.CharField(max_length=255)
        model = models.CharField(max_length=255)
        specs = models.TextField()
        image_url = models.URLField()
        source_url = models.URLField()
    