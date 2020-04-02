import scrapy
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient
import json

class get_data_user(scrapy.Spider):
    # Spider setup variables
    name = 'userInfo'
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}  # Modifying crawler's options (USER_AGENT), so crawler doens't behave like a bot and it can get response from page

    # Setting user links
    start_urls = []
    countries = {'Spain':'ES', 'USA':'US', 'India':'IN', 'Japan':'JP', 'Cambodia':'KH', 'Thailand':'TH', 'United Kingdom':'GB', 'France':'FR', 'Russian Federation':'RU', 'Germany':'DE'}  # Dictionary of countries from which we get TOP 100 users (1000 users)
    for country in countries:
        start_urls.append("https://tikrank.com/influencer/influencers?page_size=100&country={}".format(countries[country]))  # link for getting user link - region (US, IN, empty[world]), count (50 or 100)
    userLinkBefore = "https://www.tiktok.com/@"

    def parse(self, response):
        # getting user region from request url
        userRegShort = response.request.url.split("=")[2]
        for regLong, regShort in self.countries.items():
            if userRegShort == regShort:
                userRegLong = regLong
                break

        # getting user profile links and other data from tikrank.com
        jsonDataIn = json.loads(response.text)
        x = 0
        for item in jsonDataIn['data']['kols']:
            x += 1
            yield scrapy.Request(self.userLinkBefore + item['kol_unique_id'], callback=self.get_profile_data, meta={'itemNum': x, 'userLink': self.userLinkBefore + item['kol_unique_id'], 'userRegion': userRegLong})  # getting data from tiktok.com based on received profile links and passing some meta data

    # Getting user's profile data
    def get_profile_data(self, response):
        try:
            rawUserJsonData = json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userInfo']
            userInfo = {'itemNum': response.meta['itemNum'],
                        'userName': rawUserJsonData['user']['nickname'],
                        'userTag': rawUserJsonData['user']['uniqueId'],
                        'userLink': response.meta['userLink'],
                        'userDescription': rawUserJsonData['user']['signature'],
                        'userRegion': response.meta['userRegion'],
                        'userImg': rawUserJsonData['user']['avatarMedium'],
                        'userVerified': rawUserJsonData['user']['verified'],
                        'userFollowing': rawUserJsonData['stats']['followingCount'],
                        'userFollowers': rawUserJsonData['stats']['followerCount'],
                        'userLikes': rawUserJsonData['stats']['heartCount'],
                        'userVideosCount': rawUserJsonData['stats']['videoCount']
                        }
            # MongoDB setup variables
            uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
            client = MongoClient(uri)
            db = client.userData
            db.userData.update_one({'userLink': userInfo['userLink']}, {"$set": userInfo}, True)  # Updates existing or inserts new one
        except():
            print("Not able the get info about this user:" + response.meta['userLink'])

# code for runnig spider straight from script and not thru cmd
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})
process.crawl(get_data_user)
process.start()  # the script will block here until the crawling is finished
