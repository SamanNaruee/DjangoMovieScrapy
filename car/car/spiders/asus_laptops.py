import scrapy
import json
from ..items import LaptopItem
from scrapy.http import Request
from customs.Flexibles import custom_log
from django.utils import timezone

class AsusLaptopsSpider(scrapy.Spider):
    name = "asus_laptops"
    allowed_domains = ["api.digikala.com", "digikala.com"]
    start_urls = [
        "https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/asus/search/?page=1",
    ]
    crawled_urls = set()
    async def parse(self, response):
        data = json.loads(response.body)
        products = data.get('data', {}).get('products', []) if data else []
        brand = "asus"
        if not products:
            custom_log(f"No products found on page {current_page}. Stopping crawl.", self)
            return

        for product in products:
            try:
                if not product:
                    custom_log(f"There is no product: {e}", str(e))
                    continue
                source_url = f"https://digikala.com/product/{product.get('id', '')}"
                if source_url in self.crawled_urls:
                    continue

                self.crawled_urls.add(source_url)

                try:
                    laptop = LaptopItem()
                    laptop['title'] = product.get('title_fa', 'بدون نام.')
                except Exception as e:
                    custom_log(f"Error getting title: {e}", str(e))
                try:
                    laptop['price'] = product.get('default_variant', {}).get('price', {}).get('selling_price', 0)
                except Exception as e:
                    custom_log(f"Error getting price: {e}", str(e))
                try:
                    laptop['brand'] = brand.upper()
                except Exception as e:
                    custom_log(f"Error getting brand: {e}", str(e))
                try:
                    laptop['category'] = 'notebook-netbook-ultrabook'
                except Exception as e:
                    custom_log(f"Error getting category: {e}", str(e))
                try:
                    laptop['model'] = product.get('title_en', 'Unknown Model')
                except Exception as e:
                    custom_log(f"Error getting model: {e}", str(e))
                try:
                    laptop['specs'] = product.get('specifications', {})
                except Exception as e:
                    custom_log(f"Error getting specs: {e}", str(e))
                    
                try:
                    images = product.get('images', {})
                    laptop['image_urls'] = {
                        "url": images.get("main", {}).get("url", []),
                        "webp_url": images.get("main", {}).get("webp_url", []),
                    }
                except Exception as e:
                    custom_log(f"Error getting images: {e}", str(e))
                try:
                    laptop['source_url'] = source_url
                except Exception as e:
                    custom_log(f"Error getting source_url: {e}", str(e))
                try:
                    laptop['created_at'] = product.get('year', '2000/01/01')
                except Exception as e:
                    custom_log(f"Error getting created_at: {e}", str(e))
                try:
                    laptop['extra_data'] = product.get('extra_data', {})
                except Exception as e:
                    custom_log(f"Error getting extra_data: {e}", str(e))
                try:
                    laptop['crawled_at'] = product.get('crawled_at', str(timezone.now()))
                except Exception as e:
                    custom_log(f"Error getting crawled_at: {e}", str(e))
                yield laptop
            except Exception as e:
                custom_log(f"Error parsing product After assigning : {e}", str(e))

        current_page = int(response.url.split('page=')[1])
        if products:
            next_page = f"https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/{brand}/search/?page={current_page + 1}"
            if next_page not in self.crawled_urls:
                self.crawled_urls.add(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
                
