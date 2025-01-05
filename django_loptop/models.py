from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Loptop(models.Model):
        title = models.CharField(max_length=255)
        price = models.PositiveBigIntegerField()
        brand = models.CharField(max_length=255)
        model = models.CharField(max_length=255)
        category = models.CharField(max_length=255)
        specs = models.TextField()
        image_url = models.URLField()
        source_url = models.URLField()
        created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
        extra_data = models.JSONField(default=dict, null=True, blank=True)
        crawled_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
        
        def __str__(self):
            return f"{self.title} : {self.price}"
        
        def save(self, *args, **kwargs):
            if self.pk:
                old_instance = Loptop.objects.get(pk=self.pk)
                if old_instance.price != self.price:
                    LaptopPrice.objects.create(laptop=self, price=self.price)
            
            super().save(*args, **kwargs)
        
      
class LaptopPrice(models.Model):
    """
    How to use:
        laptop = Loptop.objects.get(id=laptop_id)
        price_history = laptop.price_history.all()
    """
    laptop = models.ForeignKey(Loptop, on_delete=models.PROTECT, related_name='price_history')
    price = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.laptop.title} - {self.price} at {self.created_at}"


@receiver(post_save, sender=Loptop)
def log_price_history(sender, instance, created, **kwargs):
    if created:
        LaptopPrice.objects.create(laptop=instance, price=instance.price)
