import scrapy
import json
from django_car.models import Car

class CarSpider(scrapy.Spider):
    name = "divar_car"
    allowed_domains = ["divar.ir"]
    start_urls = [
        # "https://divar.ir",
        "https://divar.ir/s/tehran/vehicles",
        # "https://api.divar.ir/v8/postlist/w/search"
    ]

    def parse(self, response):
        print_to_log(response.text())
        # print_to_log('hello')
        # for car in response.css('div.kt-post-card'):
        #     print_to_log('Into the for')
        #     title = car.css('h2.kt-post-card__title::text').get()
        #     price = car.css('div.kt-post-card__description::text').get()
        #     details = car.css('span.kt-post-card__detail::text').getall()
        #     print_to_log(title)
        #     car_data = {
        #         'title': title,
        #         'price': price,
        #         'year': details[0] if details else '',
        #         'source_url': response.urljoin(car.css('a::attr(href)').get()),
        #         'extra_data': {'details': details}
        #     }
        #     yield car_data
        return


def print_to_log(value):
    print('########################')
    print(value)
    print('########################')
