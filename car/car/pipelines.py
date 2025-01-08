# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django_loptop.models import Laptop, Phones
from datetime import datetime
from .log import custom_log
from django.db import transaction
from asgiref.sync import sync_to_async
from colorama import Fore

class LaptopPipeline:
    
    def format_date(self, date_str):
        try:    
            return datetime.strptime(date_str, "%Y/%m/%d")
        except ValueError:
            return datetime.now()
        
    @sync_to_async
    def save_item(self, item):
        with transaction.atomic():
            item['created_at'] = self.format_date(item.get('created_at'))

            obj, created = Laptop.objects.get_or_create(
                title=item['title'],
                defaults={
                    'product_id' : item['product_id'],
                    'price': item['price'],
                    'brand': item['brand'],
                    'comments': item['comments'],
                    'category': item['category'],
                    'model': item['model'],
                    'specs': item['specs'],
                    'image_urls': item['image_urls'],
                    'source_url': item['source_url'],
                    'extra_data': item['extra_data'],
                    'created_at': item['created_at'],
                    'crawled_at': item['crawled_at'],
                }
            )
            return obj

    async def process_item(self, item, spider):
        if spider.name == "laptops":
            try:
                if 'price' not in item or not item['price']:
                    custom_log(f"Missing or invalid price for laptop: {item['title']}", "price_validation")
                    return
                    
                await self.save_item(item)
                custom_log(f"Saved laptop: {item['title']}", "save_laptop", color=Fore.RED)
            except Exception as e:
                return
        return item


class PhonePipeline:
    def format_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y/%m/%d")
        except ValueError:
            return datetime.now()

    @sync_to_async
    def save_item(self, item):
        with transaction.atomic():
            item['created_at'] = self.format_date(item.get('created_at'))
            
            obj, created = Phones.objects.get_or_create(
                title=item['title'],
                defaults={
                    'product_id' : item['product_id'],
                    'price': item['price'],
                    'brand': item['brand'],
                    'category': item['category'],
                    'model': item['model'],
                    'specs': item['specs'],
                    'image_urls': item['image_urls'],
                    'source_url': item['source_url'],
                    'extra_data': item['extra_data'],
                    'created_at': item['created_at'],
                    'crawled_at': item['crawled_at'],
                }
            )
            return obj
    async def process_item(self, item, spider):              
        if spider.name == "phones":
            try:
                if 'price' not in item or not item['price']:
                    custom_log(f"Missing or invalid price for phone: {item['title']}", "price_validation")
                    return
                await self.save_item(item)
                custom_log(f"Saved phone: {item['title']}", "save_phone", color=Fore.RED)
            except Exception as e:
                custom_log("pipeline", str(e))
                return
        return item
