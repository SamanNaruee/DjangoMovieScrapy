
import scrapy
from crawling.items import Movie
from datetime import datetime

class RottenTomatoesSpider(scrapy.Spider):
    name = 'rottentomatoes'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix~genres:action']

    def parse(self, response):
        movies = response.css('table.table tr')[1:]
        
        for movie in movies:
            title = movie.css('a.unstyled.articleLink::text').get().strip()
            score = movie.css('td.tMeterScore::text').get().strip('%')
            reviews = movie.css('td.right::text').get().strip()
            movie_url = response.urljoin(movie.css('a.unstyled.articleLink::attr(href)').get())
            
            yield scrapy.Request(
                url=movie_url,
                callback=self.parse_movie_details,
                meta={
                    'title': title,
                    'score': score,
                    'reviews': reviews
                }
            )

    def parse_movie_details(self, response):
        movie_item = Movie()
        
        movie_item['title'] = response.meta['title']
        movie_item['score'] = int(response.meta['score'])
        movie_item['reviews'] = int(response.meta['reviews'])
        movie_item['url'] = response.url
        
        
        info_div = response.css('div.movie_info')
        movie_item['rating'] = info_div.css('div.meta-value::text').re_first(r'([A-Z0-9-]+)')
        
        
        release_date = info_div.css('div.meta-value time::attr(datetime)').get()
        if release_date:
            movie_item['release_date'] = datetime.strptime(release_date.split('T')[0], '%Y-%m-%d')
        
        
        movie_item['genre'] = info_div.css('div.meta-value span.genre::text').get('').strip()
        
        movie_item['director'] = info_div.css('div.meta-value a[href*="director"]::text').get('').strip()
        
        movie_item['description'] = response.css('div#movieSynopsis::text').get('').strip()
        
        cast = response.css('div.cast-item.media.inlineBlock span[title]::text').getall()
        movie_item['cast'] = ', '.join(cast) if cast else ''
        
        yield movie_item
