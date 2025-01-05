# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django_loptop.models import Loptop
from datetime import datetime
from customs.Flexibles import CustomLogger
from django.db import transaction
from asgiref.sync import sync_to_async


class LaptopPipeline:
    
    def __init__(self):
        self.logger = CustomLogger()
    
    def format_date(self, date_str):
        try:    
            return datetime.strptime(date_str, "%Y/%m/%d")
        except ValueError:
            return datetime.now()
        
    @sync_to_async
    def save_item(self, item):
        with transaction.atomic():
            item['created_at'] = self.format_date(item.get('created_at', '2000/01/01'))

            obj, created = Loptop.objects.get_or_create(
                title=item['title'],
                defaults={
                    'price': item['price'],
                    'brand': item['brand'],
                    'category': item['category'],
                    'model': item['model'],
                    'specs': item['specs'],
                    'image_url': item['image_url'],
                    'source_url': item['source_url'],
                    'extra_data': item['extra_data'],
                    'created_at': item['created_at'],
                    'crawled_at': item['crawled_at'],
                }
            )
            return obj

    async def process_item(self, item, spider):
        if spider.name == "asus_laptops":
            try:
                await self.save_item(item)
                self.logger.custom_log(f"Successfully saved laptop: {item['title']}", item['title'])
            except Exception as e:
                self.logger.custom_log(f"Error saving laptop: {str(e)}", str(e))
        return item
