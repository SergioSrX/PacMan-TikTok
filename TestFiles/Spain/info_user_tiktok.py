# -*- coding: utf-8 -*-
import scrapy
import json

class InfoUserTiktokSpider(scrapy.Spider):
    name = 'info_user_tiktok'
    allowed_domains = ['tiktok.com']
    start_urls = ['https://www.tiktok.com/@realmadrid']
    custom_settings = { 'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}

    def parse(self, response):
        yield{
        	'userName': response.css('h1.share-title::text').extract(),
            'userTag': response.css('h1.share-sub-title::text').extract(),
            'userFollowing': response.css('h2.count-infos > span.number::text')[0].extract(),
            'userFollowers': response.css('h2.count-infos > span.number::text')[1].extract(),
            'userLikes': response.css('h2.count-infos > span.number::text')[2].extract(),
            'userDescription': response.css('h2.share-desc::text').extract(),
        }
