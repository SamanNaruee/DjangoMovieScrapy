# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    
class LaptopItem(scrapy.Item): 
    title = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    model = scrapy.Field()
    specs = scrapy.Field()
    image_urls = scrapy.Field()
    source_url = scrapy.Field()
    created_at = scrapy.Field()
    crawled_at = scrapy.Field()
    extra_data = scrapy.Field()
