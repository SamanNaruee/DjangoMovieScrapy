from django.core.management.base import BaseCommand  
from scrapy.crawler import CrawlerProcess  
from scrapy.utils.project import get_project_settings  
from crawling.crawling.spiders.rottentomatoes import RottenTomatoesSpider  

class Command(BaseCommand):  
    help = 'Crawl movie data from Rotten Tomatoes'  

    def handle(self, *args, **options):  
        process = CrawlerProcess(get_project_settings())  
        process.crawl(RottenTomatoesSpider)  
        process.start()
