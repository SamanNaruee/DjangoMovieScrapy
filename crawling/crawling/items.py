# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem 
from movie.models import Movie


class MovieItem(DjangoItem):
    django_model = Movie
    image_urls = scrapy.Field()
    image = scrapy.Field()
    
