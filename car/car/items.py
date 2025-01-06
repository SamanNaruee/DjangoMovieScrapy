# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class LaptopItem(Item): 
    title = Field()
    price = Field()
    brand = Field()
    category = Field()
    model = Field()
    specs = Field()
    image_urls = Field()
    source_url = Field()
    created_at = Field()
    crawled_at = Field()
    extra_data = Field()



class PhoneItem(Item):
    title = Field()
    price = Field()
    brand = Field()
    category = Field()
    model = Field()
    specs = Field()
    image_urls = Field()
    source_url = Field()
    created_at = Field()
    extra_data = Field()
    crawled_at = Field()
