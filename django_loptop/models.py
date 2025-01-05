from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Laptop(models.Model):
        title = models.CharField(max_length=255)
        price = models.PositiveBigIntegerField(default=0)
        brand = models.CharField(max_length=255)
        model = models.CharField(max_length=255)
        category = models.CharField(max_length=255)
        specs = models.TextField()
        image_urls = models.JSONField(default=dict, blank=True)
        source_url = models.URLField()
        created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
        extra_data = models.JSONField(default=dict, null=True, blank=True)
        crawled_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
        
        def __str__(self):
            return f"{self.title} : {self.price}"
        