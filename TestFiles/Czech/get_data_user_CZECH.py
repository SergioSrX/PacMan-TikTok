import scrapy

class get_data_user(scrapy.Spider):
    name = 'userInfo'
    start_urls = ["https://www.tiktok.com/@realmadrid?lang=en"] # Todo - find out how to parse from this link, scrapy not returning html but json

    def parse(self, response):
        yield{
            'userName': response.css('h1.share-title::text'),
            'userTag': response.css('h1.share-sub-title::text'),
            #'userVerified': response.css('span.jsx-874583638').__bool__(),
            'userDescription': response.css('h2.share-desc::text'),
        }