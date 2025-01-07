from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from car.car.spiders.laptops import LaptopsSpider

class Command(BaseCommand):
    help = 'Run laptops Scrapy spider'
    
    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(LaptopsSpider)
        process.start()
        self.stdout.write(self.style.SUCCESS('Successfully scraped laptops data'))
