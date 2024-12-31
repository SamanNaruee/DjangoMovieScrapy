import scrapy
from django_car.models import Car

class CarSpider(scrapy.Spider):
    name = "divar_car"
    allowed_domains = ["divar.ir"]
    start_urls = ["https://divar.ir"]

    def parse(self, response):
        for car in rasponse.css('div.post'):
            yield {
                'title': car.css('div.post-title a::text').get(),
                'price': car.css('div.post-price::text').get(),
                'year': car.css('div.post-year::text').get(),
                'image_url': car.css('div.post-image img::attr(src)').get(),
                'source_url': car.css('div.post-title a::attr(href)').get(),
                'extra_data': {}
            }
