import scrapy
import json
from django_car.models import Car

class CarSpider(scrapy.Spider):
    name = "divar_car"
    allowed_domains = ["divar.ir"]
    start_urls = [
        # "https://divar.ir",
        "https://divar.ir/s/tehran/vehicles"
    ]

    def parse(self, response):
        for car in response.css('div.kt-post-card'):
            title = car.css('h2.kt-post-card__title::text').get()
            price = car.css('div.kt-post-card__description::text').get()
            details = car.css('span.kt-post-card__detail::text').getall()
            
            car = Car(
                title=title,
                price=price,
                year=details[0] if details else '',
                image_url=car.css('img::attr(src)').get(),
                source_url=response.urljoin(car.css('a::attr(href)').get()),
                extra_data={'details': details}
            )
            yield car