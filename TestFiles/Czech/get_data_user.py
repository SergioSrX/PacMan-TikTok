import scrapy
from scrapy.crawler import CrawlerProcess
import json

class get_data_user(scrapy.Spider):
    name = 'userInfo'
    start_urls = ["https://tikrank.com/analysis/rank?region=&count=50"]  # link for getting user link - region (US, IN, empty[world]), count (50 or 100)
    userLinkBefore = "https://www.tiktok.com/@"
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}  # Modifying crawler's options (USER_AGENT), so crawler doens't behave like a bot and it can get response from page

    def parse(self, response):
        jsonDataIn = json.loads(response.text)      # getting user profile links and other data from tikrank.com
        x = 0
        for item in jsonDataIn['data']:
            x += 1
            yield scrapy.Request(self.userLinkBefore + item['platform_unique_id'], callback=self.get_profile_data, meta={'itemNum': x, 'userLink': self.userLinkBefore + item['platform_unique_id'], 'userRegion': item['region_str'], 'userVideosCount': item['video_count_str']})     # getting data from tiktok.com based on received profile links and passing some meta data

    # Getting user's profile data
    def get_profile_data(self, response):
        try:
            user = {'itemNum': response.meta['itemNum'],
                    'userName': response.css('h1.share-title::text').extract_first(),
                    'userTag': response.css('h1.share-sub-title::text').extract_first(),
                    'userLink': response.meta['userLink'],
                    'userDescription': response.css('h2.share-desc::text').extract_first(),
                    'userRegion': response.meta['userRegion'],
                    'userImg': response.css('div.avatar-wrapper::attr(style)').extract_first().split('"')[1],
                    'userVerified': response.css('strong.jsx-1552556901::text').extract_first(default="Not verified account"),
                    'userFollowing': response.css('h2.count-infos > span.number::text')[0].extract(),
                    'userFollowers': response.css('h2.count-infos > span.number::text')[1].extract(),
                    'userLikes': response.css('h2.count-infos > span.number::text')[2].extract(),
                    'userVideosCount':  response.meta['userVideosCount']}

            # appending user data into text file in json format
            jsonDataOut = json.dumps(user)
            with open("user_data.txt", "a") as jsonFile:
                jsonFile.write(jsonDataOut + ",")
                jsonFile.close()
        except():
            print("Not able the get info about this user:" + response.meta['userLink'])

# erasing file content
open('user_data.txt', 'w').close()

# code for runnig spider straight from script and not thru cmd
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})
process.crawl(get_data_user)
process.start()  # the script will block here until the crawling is finished

# making sure text file is in proper json format
with open("user_data.txt", 'r+') as jsonFile:
    content = jsonFile.read()[:-1]  # deletes last char of the file (',')
    jsonFile.seek(0)
    jsonFile.write("[" + content + "]")
    jsonFile.close()