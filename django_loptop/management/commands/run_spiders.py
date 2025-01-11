import os  
import subprocess  
from django.core.management.base import BaseCommand  


class Command(BaseCommand):  
    help = 'Run specified Scrapy spiders'  

    def add_arguments(self, parser):  
        parser.add_argument('--phones', action='store_true', help='Run phones spider')  
        parser.add_argument('--laptops', action='store_true', help='Run laptops spider')  
        # Add additional spiders here in the future  

    def handle(self, *args, **options):  
        spider_commands = {  
            'phones': 'scrapy crawl phones',  
            'laptops': 'scrapy crawl laptops',  
            # Add more spiders as necessary  
        }  
 
        scrapy_project_path = os.path.join(  
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'car'  
        )  

        if not os.path.exists(scrapy_project_path):  
            self.stderr.write(self.style.ERROR(f'Scrapy project path does not exist: {scrapy_project_path}'))  
            return  

        original_path = os.getcwd()  

        try:  
            os.chdir(scrapy_project_path)  
            results = []  

            for spider, command in spider_commands.items():  
                if options.get(spider, False):  
                    self.stdout.write(self.style.SUCCESS(f'Starting spider: {spider}...'))  
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)  
                    results.append((result, spider))  

            for result, spider_name in results:  
                if result.returncode == 0:  
                    self.stdout.write(self.style.SUCCESS(f'Successfully scraped data with {spider_name} spider.'))  
                    self.stdout.write(result.stdout)  
                else:  
                    self.stderr.write(self.style.ERROR(f'Error running {spider_name} spider: {result.stderr}'))  

        except Exception as e:  
            self.stderr.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))  

        finally:  
            os.chdir(original_path)  
            self.stdout.write(self.style.SUCCESS('Returned to original directory.'))
