# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django_car.models import Car


class CarPipeline:
    def process_item(self, item, spider):
        model_instance = Car(
            title = item.get('title'),
            price = item.get('price'),
            year = item.get('year'),
            image_url = item.get('image_url'),
            source_url = item.get('source_url'),
            extra_data = item.get('extra_data'),
        )
        model_instance.save()
        return item
    