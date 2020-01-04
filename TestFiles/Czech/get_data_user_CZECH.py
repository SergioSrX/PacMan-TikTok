import scrapy
import json


class get_data_user(scrapy.Spider):
    name = 'userInfo'
    start_urls = ["https://www.tiktok.com/@realmadrid?lang=en"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}  # Modifying crawler's options (USER_AGENT), so crawler doens't behave like a bot and it can get response from page
    videos_url = "https://m.tiktok.com/share/item/list?secUid=MS4wLjABAAAAdi4wJZtAiIre_rQ1KiFteDmtrGBDIyoleHRNsjL14-Enf8aVfkLUJ0l_LcJPZkiv&id=6693776501107033094&type=1&count=30&minCursor=0&maxCursor=0&shareUid=&_signature=HSu7DgAgEBZo2jBQv.o2iB0ruhAAEM."  # Link from videos in json format

    def parse(self, response):
        yield {
            'userName': response.css('h1.share-title::text').extract_first(),
            'userTag': response.css('h1.share-sub-title::text')[0].extract() + response.css('h1.share-sub-title::text')[
                1].extract(),  # userTag is made out of two elements --> @ and "user tag"
            'userDescription': response.css('h2.share-desc::text').extract_first(),
            'userImg': response.css('div.jsx-2177493926::attr(style)').extract_first().split('"')[1],
            # gets css of tag, then parsed into background-img link
            'userVerified': response.css('span.jsx-874583638::text').extract_first(default="Not verified account"),
            # if tag that says: 'user is verified' is missing, default option is chosen
            'userFollowing': response.css('p.count-infos > span.number::text')[0].extract(),
            'userFollowers': response.css('p.count-infos > span.number::text')[1].extract(),
            'userLikes': response.css('p.count-infos > span.number::text')[2].extract(),
        }
        yield scrapy.Request(self.videos_url, callback=self.parse_videos_json)

    # Getting top 10 user's video links
    def parse_videos_json(self, response):
        data = json.loads(response.text)
        x = 0
        for item in data['body']['itemListData']:
            if x <= 9:
                yield {
                    'userVideo': item['itemInfos']['video']['urls'][0]
                }
                x += 1
