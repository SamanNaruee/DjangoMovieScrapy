# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django_car.models import Car
import logging

class CarPipeline:
    def process_item(self, item, spider):
        logging.info(f"Processing item: {item}")
        model_instance = Car(
            title=item['title'],
            price=item['price'],
            year=item['year'],
            image_url=item['image_url'],
            source_url=item['source_url'],
            extra_data=item['extra_data']
        )
        model_instance.save()
        logging.info(f"Saved car: {model_instance.title}")
        return item

from django_loptop.models import Loptop
import logging

class LoptopPipeline:
    def process_item(self, item, spider):
        logging.info(f"Processing item: {item}")
        model_instance = Loptop(
            title=item['title'],
            price=item['price'],
            brand=item['brand'],
            model=item['model'],
            specs=item['specs'],
            image_url=item['image_url'],
            source_url=item['source_url'],
            year = item['year'],
            extra_data=item['extra_data']
        )
        model_instance.save()
        logging.info(f'Saved loptop: {model_instance.title}')
        custom_log(f"Saved loptop: {model_instance.title}")
        return item


def custom_log(value):
    print("##################################################")
    print(value)
    print("##################################################")