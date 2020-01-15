import scrapy
import json


class UserinfoSpider(scrapy.Spider):
    name = 'userinfo'
    allowed_domains = ['tiktok.com']
    start_urls = ['http://tiktok.com/@therock']
    custom_settings = { 'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}

    def parse(self, response):
        self.log("This is what I found:")
        yield{
            "ShowName": response.css('h1.share-title::text').extract(),
            "UserName": response.css('h1.share-sub-title::text').extract(),
            "UserFollowing": response.css('span.number::text')[0].extract(),
            "UserFollowers": response.css('span.number::text')[1].extract(),
            "UserLikes": response.css('span.number::text')[2].extract(),
            "UserDesc": response.css('h2.share-desc::text').extract(),
        }
