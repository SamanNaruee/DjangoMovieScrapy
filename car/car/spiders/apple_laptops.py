import scrapy  
import json  
from ..items import LaptopItem  
from scrapy.http import Request  
from customs.Flexibles import custom_log  
from django.utils import timezone  
from colorama import Fore, Style  
from django_loptop.models import Laptop
from asgiref.sync import sync_to_async  

color = Fore.RED  

class AppleLaptopsSpider(scrapy.Spider):  
    name = "apple_laptops"  
    allowed_domains = ["api.digikala.com", "digikala.com"]  
    start_urls = [  
        "https://api.digikala.com/v1/categories/notebook-netbook-ultrabook/brands/apple/search/?page=1",  
    ]  
    crawled_urls = set()  

    def parse(self, response):
        pass