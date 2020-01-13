# -*- coding: utf-8 -*-
import scrapy


class InfoUserTiktokSpider(scrapy.Spider):
    name = 'info_user_tiktok'
    allowed_domains = ['tiktok.com']
    start_urls = ['http://tiktok.com/@realmadrid']

    def parse(self, response):
        yield{
        	'userName': response.css('h1.share-title::text'),
            'userTag': response.css('h1.share-sub-title::text'),
            'userFollowing': response.css('h2.count-infos > span.number::text')[0].extract(),
            'userFollowers': response.css('h2.count-infos > span.number::text')[1].extract(),
            'userLikes': response.css('h2.count-infos > span.number::text')[2].extract(),
            'userDescription': response.css('h2.share-desc::text'),
        }
