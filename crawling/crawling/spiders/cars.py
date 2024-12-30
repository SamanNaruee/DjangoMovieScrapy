import scrapy
from divar_crawler.models import Cars

class CarSpider(scrapy.Spider):
    name = 'cars' 
    allowed_domains = ['divar.ir']
    start_urls = ['https://divar.ir/s/tehran/car']  

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
