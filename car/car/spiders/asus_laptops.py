import scrapy
import json
from car.items import LaptopItem
from django_loptop.models import Loptop
from customs.Flexibles import custom_log

class AsusLaptopsSpider(scrapy.Spider):
    """
    Extra help:
        1. unic all products to ensure will not recieve duplicate data.
        2. scrawl extra unset django.model fields in extra_data JsonField.
        3. Fix jumping bug related to empty or buggy pages.
        4. Make this logic more Flexible. break it to the small pices.
        5. Fix shuffled data that scrawled in non-order by paginations and brands.
    """
    name = "asus_laptops"
    allowed_domains = [
        "api.digikala.com",
        "digikala.com",
        "www.digikala.com",
        ]
    start_urls = [
        "https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/asus/search/?page=1",
    ]

    async def parse(self, response):
        data = json.loads(response.body)
        products = data.get('data', {}).get('products', [])
        brands = ['asus', 'acer', 'dell', 'apple', 'msi']
        
        for brand in brands:
            try:
                for product in products:
                    try:
                        laptop = LaptopItem()
                        laptop['title'] = product.get('title_fa', '')
                        laptop['price'] = product.get('default_variant', {}).get('price', {}).get('selling_price', '')
                        laptop['brand'] = f'{brand}'.upper()
                        laptop['model'] = product.get('title_en', '')
                        laptop['specs'] = product.get('specifications', {})
                        laptop['image_url'] = product.get('image', {}).get('url', '')
                        laptop['source_url'] = f"https://digikala.com/product/{product.get('id')}" # Make this one unic
                        laptop['year'] = product.get('year', '2000/01/01')
                        laptop['extra_data'] = product.get('extra_data', {}) 
                        yield laptop
                    except Exception as e:
                        custom_log(f"asus_laptopspy:\n\n{e}", )

                # Get current page number from the URL
                current_page = int(response.url.split('page=')[1])
                
                # Check if there are more products
                if products:
                    custom_log(f"Scraped page {current_page}")
                    # Construct URL for next page
                    next_page = f"https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/{brand}/search/?page={current_page + 1}"
                    custom_log(f"Next page URL: {next_page}")
                    yield scrapy.Request(next_page, callback=self.parse)
                    custom_log(f"Parsed next page URL: {next_page}")
            except Exception as e:
                custom_log(str(e), f'In first try-exept got this error for brand{brand}')
