import scrapy
import json
from car.items import LaptopItem

class AsusLaptopsSpider(scrapy.Spider):
    name = "asus_laptops"
    allowed_domains = [
        "api.digikala.com",
        "digikala.com",
        "www.digikala.com",
        ]
    start_urls = [
        "https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/asus/search/?page=1",
    ]

    def parse(self, response):
        data = json.loads(response.body)
        # products = data.get('data', {}).get('products', [])
        
        # for product in products:
        #     laptop = LaptopItem()
        #     laptop['title'] = product.get('title_fa', '')
        #     laptop['price'] = product.get('default_variant', {}).get('price', {}).get('selling_price', '')
        #     laptop['brand'] = 'ASUS'
        #     laptop['model'] = product.get('title_en', '')
        #     laptop['specs'] = product.get('specifications', {})
        #     laptop['image_url'] = product.get('image', {}).get('url', '')
        #     laptop['source_url'] = f"https://digikala.com/product/{product.get('id')}"
        #     yield laptop
        
        yield {
            'data' : data
        }