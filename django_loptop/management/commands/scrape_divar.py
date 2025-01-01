from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from car.car.spiders.divar_car import CarSpider

class Command(BaseCommand):
    help = 'Run Divar car Scrapy spider'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(CarSpider)
        process.start()
        self.stdout.write(self.style.SUCCESS('Successfully scraped Divar car data'))

