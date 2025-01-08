import scrapy  
import json  
from ..items import PhoneItem  
from scrapy.http import Request  
from ..log import custom_log 
from django.utils import timezone  
from colorama import Fore

class PhonesSpider(scrapy.Spider):  
    name = "phones"  
    allowed_domains = ["api.digikala.com", "digikala.com"]  
    all_brands = ["samsung", "apple", "xiaomi", "huawei", "nokia", "honor", "motorola", "asus", "oneplus"]
    crawled_urls = set()  

    def start_requests(self):  
        for brand in self.all_brands:  
            url = f"https://api.digikala.com/v1/categories/mobile-phone/brands/{brand}/search/?page=1"  
            yield scrapy.Request(url, callback=self.parse, meta={'brand': brand, 'current_page': 1})  

    def parse(self, response):  
        brand = response.meta['brand']  
        current_page = response.meta['current_page']  
        data = json.loads(response.body)
        products = data.get('data', {}).get('products', []) if data else []  

        if not products:  
            return  

        for product in products:  
            try:  
                if not product:  
                    continue  
                
                product_id = product.get('id', '')
                source_url = f"https://digikala.com/product/dkp-{product_id}"  
                if source_url in self.crawled_urls:  
                    continue  
                
                self.crawled_urls.add(source_url)  
                
                # Get detailed product info
                detailed_url = f"https://api.digikala.com/v2/product/{product_id}/"
                yield scrapy.Request(
                    detailed_url,
                    callback=self.parse_phone_details,
                    meta={
                        'brand': brand,
                        'basic_product': product,
                        'source_url': source_url
                    }
                )

            except Exception as e:  
                custom_log("exception in parse: " + str(e), "parse_exception")
                continue  

        if products:  
            next_page = f"https://api.digikala.com/v1/categories/mobile-phone/brands/{brand}/search/?page={current_page + 1}"  
            if next_page not in self.crawled_urls:  
                self.crawled_urls.add(next_page)  
                yield scrapy.Request(next_page, callback=self.parse, meta={'brand': brand, 'current_page': current_page + 1})

    def parse_phone_details(self, response):
        data = json.loads(response.body)
        product = response.meta['basic_product']
        brand = response.meta['brand']
        source_url = response.meta['source_url']

        phone = PhoneItem()
        phone['title'] = product.get('title_fa', 'بدون نام.')
        
        try:  
            default_variant = product.get('default_variant', {})  
            if isinstance(default_variant, dict):  
                price = default_variant.get('price', {}).get('selling_price', 0)  
                phone['price'] = int(price) if price else 0  
            else:  
                custom_log("Invalid default_variant format", "price_validation")
                return None
        except Exception as e:  
            custom_log(f"Error getting price in 'parse_phone' : {e}", str(e))  
            return None
        
        phone['brand'] = str(brand.upper())  
        phone['category'] = 'mobile-phone'  
        phone['model'] = str(product.get('title_en', 'Unknown Model'))  
        phone['specs'] = dict(product.get('specifications', {}))  
                
        try:  
            images = product.get('images', {})  
            phone['image_urls'] = {  
                "url": str(images.get("main", {}).get("url", "")),  
                "webp_url": str(images.get("main", {}).get("webp_url", "")),  
            }  
        except Exception as e:
            custom_log(f"Error getting images: {e}", "image_validation")
            return None
                
        phone['source_url'] = str(source_url)  
        phone['product_id'] = str(product.get('id', ''))
        phone['created_at'] = str(product.get('year', '2000/01/01'))  
        phone['extra_data'] = dict(product.get('extra_data', {}))  
        phone['crawled_at'] = str(timezone.now())  

        if all([phone['title'], phone['price'], phone['brand'], phone['image_urls']]):
            custom_log(f"Phone item: {phone}", "phone_item")
            yield phone
        else:
            custom_log(f"Skipping incomplete phone item: {phone['title']}", "incomplete_item")

