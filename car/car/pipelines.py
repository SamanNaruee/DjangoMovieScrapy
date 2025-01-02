# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django_loptop.models import Loptop
import logging

from django.db import transaction
from asgiref.sync import sync_to_async



class LaptopPipeline:
    @sync_to_async
    def save_item(self, item):
        with transaction.atomic():
            model_instance = Loptop(
                title=item['title'],
                price=item['price'],
                brand=item['brand'],
                model=item['model'],
                specs=item['specs'],
                image_url=item['image_url'],
                source_url=item['source_url'],
                extra_data=item['extra_data'],
                year=item['year']
            )
            model_instance.save()
            return model_instance

    async def process_item(self, item, spider):
        if spider.name == "asus_laptops":
            try:
                await self.save_item(item)
                custom_log(f"Successfully saved laptop: {item['title']}")
            except Exception as e:
                custom_log(f"Error saving laptop: {str(e)}")
        return item


def custom_log(value):
    print("##################################################")
    print("pipelines.py:\n\n", value)
    print("##################################################")