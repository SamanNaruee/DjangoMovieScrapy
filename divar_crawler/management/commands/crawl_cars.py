from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawling.crawling.spiders.cars import CarsSpider

class Command(BaseCommand):
    help = 'Crawl cars data'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(CarsSpider)
        process.start()
