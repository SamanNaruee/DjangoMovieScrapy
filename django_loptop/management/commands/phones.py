from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from car.car.spiders.phones_spider import PhonesSpider

class Command(BaseCommand):
    help = 'Run phones Scrapy spider'
    
    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(PhonesSpider)
        process.start()
        self.stdout.write(self.style.SUCCESS('Successfully scraped Phones data'))
