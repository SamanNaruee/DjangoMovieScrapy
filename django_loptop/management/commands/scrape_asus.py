from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from car.car.spiders.asus_laptops import AsusLaptopsSpider

class Command(BaseCommand):
    help = 'Run Asus laptops Scrapy spider'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(AsusLaptopsSpider)
        process.start()
        self.stdout.write(self.style.SUCCESS('Successfully scraped Asus laptops data'))
