import scrapy
import json
from ..items import LaptopItem
from scrapy.http import Request
from customs.Flexibles import custom_log
from django.utils import timezone

class AllLaptopsSpider(scrapy.Spider):
    name = "all_laptops"
    allowed_domains = ["api.digikala.com", "digikala.com"]
    all_brands = ["asus", "apple", "dell", "hp", "lenovo", "msi", "samsung", "sony", "toshiba", "xiaomi"]
    crawled_urls = set()



    async def parse(self, response):
        data = json.loads(response.body)
        products = data.get('data', {}).get('products', []) if data else []
        brand = response.meta['brand']

        if not products:
            custom_log(f"No products found for {brand}. Moving to next brand.", self)
            return

        for product in products:
            try:
                if not product:
                    continue
                    
                source_url = f"https://digikala.com/product/{product.get('id', '')}"
                if source_url in self.crawled_urls:
                    continue
                
                self.crawled_urls.add(source_url)
                laptop = LaptopItem()
                laptop['title'] = product.get('title_fa', 'بدون نام.')

                try:  
                    default_variant = product.get('default_variant', {})  
                    if isinstance(default_variant, dict):  
                        price = default_variant.get('price', {}).get('selling_price', 0)  
                        laptop['price'] = price if price else 0  
                    else:  
                        custom_log("default_variant is not a dictionary", self)  
                        continue
                except Exception as e:  
                    custom_log(f"Error getting price: {e}", str(e))  
                        
                laptop['brand'] = brand.upper()
                laptop['category'] = 'notebook-netbook-ultrabook'
                laptop['model'] = product.get('title_en', 'Unknown Model')
                laptop['specs'] = product.get('specifications', {})
                laptop['image_urls'] = {
                    "url": product.get('images', {}).get("main", {}).get("url", []),
                    "webp_url": product.get('images', {}).get("main", {}).get("webp_url", []),
                }
                laptop['source_url'] = source_url
                laptop['created_at'] = product.get('year', '2000/01/01')
                laptop['extra_data'] = product.get('extra_data', {})
                laptop['crawled_at'] = str(timezone.now())
                
                yield laptop

            except Exception as e:
                custom_log(f"Error parsing product: {e}", str(e))

        current_page = int(response.url.split('page=')[1])
        next_page = f"https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/{brand}/search/?page={current_page + 1}"
        
        if next_page not in self.crawled_urls and products:
            self.crawled_urls.add(next_page)
            yield scrapy.Request(next_page, callback=self.parse, meta={'brand': brand})
