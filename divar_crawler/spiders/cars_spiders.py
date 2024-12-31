import scrapy  
import json

class CarsSpider(scrapy.Spider):  
    name = 'cars'  # This should match the name you're trying to run  
    allowed_domains = ['divar.ir']  
    start_urls = ['https://divar.ir/s/tehran/car']  
    
    def __init__(self):
        super().__init__()
        self.cars_data = []

    def parse(self, response):  
        # Extract car listings  
        for car in response.css('div.card-item'):  
            price = car.css('div.card-item-price::text').get()  
            price_value = self.convert_price(price)  

            if price_value and 300_000_000 <= price_value <= 400_000_000:  
                title = car.css('h2.card-title::text').get()  
                link = car.css('a.card-item-link::attr(href)').get()  

                # Store car data in list
                car_data = {
                    'title': title,
                    'price': price_value,
                    'link': link
                }
                self.cars_data.append(car_data)
                self.log(f'Collected car: {title} - {price_value} تومان')  

        # Handle pagination  
        next_page = response.css('a.pagination-next::attr(href)').get()  
        if next_page is not None:  
            yield response.follow(next_page, self.parse)
        else:
            # When no more pages, save all data to JSON file
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(self.cars_data, f, ensure_ascii=False, indent=4)

    def convert_price(self, price_str):  
        """Convert price from string to integer."""  
        if price_str:  
            return int(price_str.replace('تومان', '').replace(',', '').strip())  
        return None
