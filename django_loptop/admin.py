from django.contrib import admin
from django_loptop.models import Laptop

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'brand', 'model', 'category', 'specs', 'image_urls', 'source_url', 'created_at', 'extra_data', 'crawled_at')
    list_filter = ('brand', 'category', 'created_at', 'crawled_at')
    search_fields = ('title', 'brand', 'model', 'category')
    ordering = ('-created_at',)