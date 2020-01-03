import scrapy

class get_data_user(scrapy.Spider):
    name = 'userInfo'
    start_urls = ["https://www.tiktok.com/@realmadrid?lang=en"]
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}  # Modifying crawler's options (USER_AGENT), so crawler doens't behave like a bot and it can get response from page

    def parse(self, response):
        yield{
            'userName': response.css('h1.share-title::text').extract_first(),
            'userTag': response.css('h1.share-sub-title::text')[0].extract() + response.css('h1.share-sub-title::text')[1].extract(),  # userTag is made out of two elements --> @ and "user tag"
            'userDescription': response.css('h2.share-desc::text').extract_first(),
            'userImg':  response.css('div.jsx-2177493926::attr(style)').extract_first(),  # TODO parse just background-img link
            'userVerified': response.css('span.jsx-874583638::text').extract_first(default="Not verified account"),
            'userFollowing': response.css('p.count-infos > span.number::text')[0].extract(),
            'userFollowers': response.css('p.count-infos > span.number::text')[1].extract(),
            'userLikes': response.css('p.count-infos > span.number::text')[2].extract(),
            # TODO get top 10 recent videos
        }
