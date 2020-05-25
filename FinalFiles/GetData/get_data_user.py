import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spidermiddlewares.httperror import HttpError
from pymongo import MongoClient
from time import sleep as pause
from datetime import datetime as time
from Naked.toolshed.shell import muterun_js

class get_data_user(scrapy.Spider):
    # Spider setup variables
    name = 'userInfo'
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}  # Modifying crawler's options (USER_AGENT), so crawler doens't behave like a bot and it can get response from page

    # MongoDB setup variables
    uri = 'mongodb+srv://test:test123456@cluster0-yqf6t.mongodb.net/test?retryWrites=true&w=majority'  # mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority
    client = MongoClient(uri)
    db = client.userData
    # Setting user links
    start_urls = []
    countries = {'Spain':'ES'}  # 'Spain':'ES' ,'USA':'US', 'India':'IN', 'Japan':'JP', 'Cambodia':'KH', 'Thailand':'TH', 'United Kingdom':'GB', 'France':'FR', 'Russian Federation':'RU', 'Germany':'DE' Dictionary of countries from which we get TOP 100 users (1000 users)
    for country in countries:
        start_urls.append("https://tikrank.com/influencer/influencers?page_size=10&country={}".format(countries[country]))  # link for getting user link - region (US, IN, empty[world]), count (50 or 100)
    userLinkBefore = "https://www.tiktok.com/@"

    # Method for getting user profile links from Tiktank.com
    def parse(self, response):
        # Getting user region from request url
        userRegShort = response.request.url.split("=")[2]
        for regLong, regShort in self.countries.items():
            if userRegShort == regShort:
                userRegLong = regLong
                break

        # Loading user profile links and other data from tikrank.com
        jsonDataIn = json.loads(response.text)
        for item in jsonDataIn['data']['kols']:
            # Calling method get_profile_data and passing some meta data
            yield scrapy.Request(self.userLinkBefore + item['kol_unique_id'], callback=self.get_profile_data, meta={'userLink': self.userLinkBefore + item['kol_unique_id'], 'userRegion': userRegLong}, errback=self.get_profile_data_err_handler)

    # Method for handling errors of scraping user's profile data
    def get_profile_data_err_handler(self, failure):
        if failure.check(HttpError):
            self.logger.error('Not able to get data from this user Url: ' + failure.value.response.url)

    # Method for getting user's profile data
    def get_profile_data(self, response):
        pause(0.5)  # 0.5sec pause so we dont get timeout on Tiktok server
        rawUserData = json.loads(response.css('script#__NEXT_DATA__::text')[0].re('.*')[0])['props']['pageProps']['userInfo']
        userInfo = {'userID': rawUserData['user']['id'],
                    'userSecUid': rawUserData['user']['secUid'],
                    'userName': rawUserData['user']['nickname'],
                    'userTag': rawUserData['user']['uniqueId'],
                    'userLink': response.meta['userLink'],
                    'userDescription': rawUserData['user']['signature'],
                    'userRegion': response.meta['userRegion'],
                    'userImg': rawUserData['user']['avatarMedium'],
                    'userVerified': rawUserData['user']['verified'],
                    }

        # Updates existing user data or inserts new one
        self.db.userData.update_one({'userID': userInfo['userID']},
                               {'$set': userInfo,
                               '$push':
                                    {'userStats':
                                         {'datetime': time.utcnow().strftime("%d-%m-%Y %X"),
                                          'userFollowing': rawUserData['stats']['followingCount'],
                                          'userFollowers': rawUserData['stats']['followerCount'],
                                          'userLikes': rawUserData['stats']['heartCount'],
                                          'userVideosCount': rawUserData['stats']['videoCount']
                                        }
                                    }
                                }, True)

        # Generating user media singature and verifyFp using nodeJS browser.js script. Script is called using Naked lib
        userMediaLink = "https://m.tiktok.com/api/item_list/?count=30&id=" + userInfo['userID'] + "&type=1&secUid=" + userInfo['userSecUid'] + "&maxCursor=0&minCursor=0&sourceType=8&appId=1233&region=CZ&language=cs"
        signatureGenOut = muterun_js('../../nodeJS/node_modules/tiktok-signature/browser.js', '"' + userMediaLink + '"')   # calling browser.js script
        userMediaSignature = json.loads(signatureGenOut.stdout.decode("utf-8"))['signature']
        userMediaVerifyFp = json.loads(signatureGenOut.stdout.decode("utf-8"))['verifyFp']
        if signatureGenOut.exitcode == 0:
            # Calling method get_media_data and passing some meta data
            yield scrapy.Request(userMediaLink + "&verifyFp=" + userMediaVerifyFp + "&_signature=" + userMediaSignature, callback=self.get_media_data, meta={'userID': userInfo['userID']})

    # Method for getting user's media data
    def get_media_data(self, response):
        rawUserMediaData = json.loads(response.text)['items']
        userMediaInfo = []
        for item in rawUserMediaData:
            # Error handling if video has no hash tags
            try:
                challenges = item['challenges']
            except KeyError:
                challenges = []

            userMediaInfo.append({
                'videoData': {
                    'videoID': item['id'],
                    'videoDescription': item['desc'],
                    'videoDuration': item['video']['duration'],
                    'videoImg': item['video']['cover'],
                    'videoLink': item['video']['playAddr']
                },
                'musicData': {
                    'musicID': item['music']['id'],
                    'musicName': item['music']['title'],
                    'musicLink': item['music']['playUrl'],
                    'musicImg': item['music']['coverMedium'],
                    'musicIsOriginal': item['music']['original']    # If true video is without music and uses original sound
                },
                'hashtagsData': challenges,
                'videoStats': {
                    'videoLikes': item['stats']['diggCount'],
                    'videoShares': item['stats']['shareCount'],
                    'videoComments': item['stats']['commentCount'],
                    'videoViews': item['stats']['playCount']
                }
            })

        # Saving user's media data
        self.db.userData.update_one({'userID': response.meta['userID']}, {'$set': {'mediaData': userMediaInfo}}, True)


# code for runnig spider straight from script and not with CLI
process = CrawlerProcess(settings={})
process.crawl(get_data_user)
process.start()  # the script will block here until the crawling is finished
