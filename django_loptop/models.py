from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Loptop(models.Model):
        title = models.CharField(max_length=255)
        price = models.PositiveBigIntegerField()
        brand = models.CharField(max_length=255)
        model = models.CharField(max_length=255)
        category = models.CharField(max_length=255)
        specs = models.TextField()
        image_url = models.URLField()
        source_url = models.URLField()
        created_at = models.DateTimeField(null=True, blank=True)
        extra_data = models.JSONField(default=dict, null=True, blank=True)
        scrawled_at = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
            return f"{self.title} : {self.price}"
        
        


class LaptopPrice(models.Model):
    """
    How to use:
        laptop = Loptop.objects.get(id=laptop_id)
        price_history = laptop.price_history.all()
    """
class LaptopPrice(models.Model):  
    laptop = models.ForeignKey(Loptop, on_delete=models.PROTECT, related_name='price_history')  # Add related_name for easy access  
    price = models.PositiveBigIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:  
        ordering = ['-created_at']

    def __str__(self):  
        return f"{self.laptop.title} - {self.price} at {self.created_at}"  

@receiver(post_save, sender=Loptop)
def create_laptop_price(sender, instance, created, **kwargs):
    if created:
        LaptopPrice.objects.create(price=instance.price)