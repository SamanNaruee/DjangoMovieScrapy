import scrapy  
import json  
from ..items import LaptopItem  
from scrapy.http import Request  
from ..log import custom_log 
from django.utils import timezone  

class LaptopsSpider(scrapy.Spider):  
    name = "laptops"  
    allowed_domains = ["api.digikala.com", "digikala.com"]  
    all_brands = ["asus", "apple", "dell", "hp", "lenovo", "msi", "samsung", "sony", "toshiba", "xiaomi"]  
    crawled_urls = set()  

    def start_requests(self):  
        for brand in self.all_brands:  
            url = f"https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/{brand}/search/?page=1"  
            yield scrapy.Request(url, callback=self.parse, meta={'brand': brand, 'current_page': 1})  

    def parse(self, response):  
        brand = response.meta['brand']  
        current_page = response.meta['current_page']  
        data = json.loads(response.body)  
        products = data.get('data', {}).get('products', []) if data else []  

        if not products:  
            custom_log(f"No products found for {brand} on page {current_page}. Stopping crawl.", self)  
            return  

        for product in products:  
            try:  
                if not product or not product['default_variant']:  
                    continue  
                
                product_id = product.get('id', '')
                source_url = f"https://digikala.com/product/dkp-{product_id}"
                if source_url in self.crawled_urls:  
                    continue  
                
                self.crawled_urls.add(source_url)  
                detailed_api = f'https://api.digikala.com/v2/product/{product_id}/'
                yield scrapy.Request(
                    detailed_api,
                    callback=self.parse_laptop_details,
                    meta={
                        'brand': brand,
                        'basic_product': product,
                        'source_url': source_url,
                        'product_id': product_id,
                    }
                )
            except Exception as e:  
                custom_log(f"Error parsing product: {e}", str(e))  

        if products:  
            next_page = f"https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/{brand}/search/?page={current_page + 1}"  
            if next_page not in self.crawled_urls:  
                self.crawled_urls.add(next_page)  
                yield scrapy.Request(next_page, callback=self.parse, meta={'brand': brand, 'current_page': current_page + 1})
    def parse_laptop_details(self, response):
        data = json.loads(response.body)
        product = response.meta['basic_product']
        brand = response.meta['brand']
        source_url = response.meta['source_url']
        product_id = response.meta['product_id']

        laptop = LaptopItem()  
        laptop['title'] = product.get('title_fa', 'بدون نام.')  
        

        default_variant = product.get('default_variant', {})  
        if default_variant and isinstance(default_variant, dict):  
            price = default_variant.get('price', {}).get('selling_price', 0)  
            laptop['price'] = price if price else 0  
        else:  
            return   

            
        laptop['brand'] = brand.upper()  
        laptop['category'] = 'notebook-netbook-ultrabook'  
        laptop['model'] = product.get('title_en', 'Unknown Model')  
        laptop['specs'] = product.get('specifications', {})   
              
        images = product.get('images', {})  
        laptop['image_urls'] = {  
            "url": images.get("main", {}).get("url", []),  
            "webp_url": images.get("main", {}).get("webp_url", []),  
        }  
        laptop['product_id'] = product_id
        laptop['source_url'] = source_url  
        laptop['created_at'] = product.get('year', '2000/01/01')  
        laptop['comments'] = product.get('last_comments', [])
        laptop['extra_data'] = product.get('extra_data', {})  
        laptop['crawled_at'] = str(timezone.now())  
        
        yield laptop  
