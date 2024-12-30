import scrapy
from divar_crawler.models import Cars

class CarsSpider(scrapy.Spider):
    name = 'cars'  # This name must match what you use in crawl command
    allowed_domains = ['your-domain.com']  # Replace with actual domain
    start_urls = ['https://your-domain.com/cars']  # Replace with actual URL

    def parse(self, response):
        self.log(f'Response status: {response.status}') 
        for car in response.css('.post-card-item'):
            item = Cars(
                titel=car.css('title-selector::text').get(),
                price=self.convert_price(car.css('price-selector::text').get()),
                linK=car.css('link-selector::attr(href)').get()
            )
            item.save()

    def convert_price(self, price_str):
        """Convert price from string to integer."""
        if price_str:
            return int(price_str.replace('تومان', '').replace(',', '').strip())
        return None
