import scrapy  
from divar_crawler.models import Car  
import os  
import django  

# Set up the Django environment  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  
django.setup()  

class CarsSpider(scrapy.Spider):  
    name = 'cars'  # This should match the name you're trying to run  
    allowed_domains = ['divar.ir']  
    start_urls = ['https://divar.ir/s/tehran/car']  

    def parse(self, response):  
        # Extract car listings  
        for car in response.css('div.card-item'):  
            price = car.css('div.card-item-price::text').get()  
            price_value = self.convert_price(price)  

            if price_value and 300_000_000 <= price_value <= 400_000_000:  
                title = car.css('h2.card-title::text').get()  
                link = car.css('a.card-item-link::attr(href)').get()  

                # Save each car instance in the database  
                Car.objects.create(  
                    title=title,  
                    price=price_value,  
                    link=link  
                )  
                self.log(f'Saved car: {title} - {price_value} تومان')  

        # Handle pagination  
        next_page = response.css('a.pagination-next::attr(href)').get()  
        if next_page is not None:  
            yield response.follow(next_page, self.parse)  

    def convert_price(self, price_str):  
        """Convert price from string to integer."""  
        if price_str:  
            return int(price_str.replace('تومان', '').replace(',', '').strip())  
        return None