# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from movie.models import Movie

class CrawlingPipeline:
    def process_item(self, item, spider):
        return item


class MovePipeline:
    def process_item(self, item, spider):
        Movie.object.create(
            title=item['title'],
            genre=item['genre'],
            rating=item['score'],
            year=2018,
            release_date=item['release_date'],
            director=item['director'],
        ).save()
        return item
