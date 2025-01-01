import scrapy
import json
from django_car.models import Car

class CarSpider(scrapy.Spider):
    name = "divar_car"
    allowed_domains = [
            "digikala.com",
            "api.digikala.com",
            "www.digikala.com",
            "divar.ir",
            "api.divar.ir",
        ]
    start_urls = [
        "https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/asus/search/?page=1",
    ]

    def parse(self, response):
        yield {
            'data' : json.loads(response.body)
        }

def print_to_log(value):
    print('########################')
    print(value)
    print('########################')
