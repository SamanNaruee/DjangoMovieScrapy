import scrapy
from divar_crawler.models import Cars
from django.utils import timezone
import os
import django
import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "best_movies.settings")
django.setup()


class CarsSpider(scrapy.Spider):
    name = 'cars'
    ALLOWED_HOSTS = ['divar.ir']
    start_urls = ['https://divar.ir/s/tehran/car']
    
    def parse(self, response):
        for car in response.css('div.card-item'):
            price = car.css('div.card-item-price::text').get()
            price_value = self.convert_price(price)
            
            if price_value and 300000000 <= price_value <= 400000000:
                title = car.css('h2.card-item::text').get()
                link = car.css('a.card-item-link::attr(href)').get()
                
                Cars.objects.create(
                    titel=title,
                    price=price,
                    linK=link,
                ).save()
                
                self.logger.info(f'\nCar: {title} saved')
        
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    
    
    def convert_price(self, price):
        """convert price to integer"""
        if price:
            try:
                price = int(price.replace('تومان', '').replace(',', '').strip())
            except ValueError:
                price = null
            return price
        return null