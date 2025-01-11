# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import sys  
import os  
import django  

DJANGO_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(DJANGO_PROJECT_PATH)  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'best_movies2.settings')  
