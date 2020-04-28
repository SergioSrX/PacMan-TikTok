import json
import scrapy
from scrapy.crawler import CrawlerProcess
from pymongo import MongoClient
from time import sleep as pause
from datetime import datetime as time
from Naked.toolshed.shell import muterun_js

class get_data_user(scrapy.Spider):
    # Spider setup variables
    name = 'userInfo'
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}  # Modifying crawler's options (USER_AGENT), so crawler doens't behave like a bot and it can get response from page

    # MongoDB setup variables
    uri = 'mongodb+srv://packman:MIB123456@packman-mib-wil2x.azure.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client.userData

    # Setting user links
    start_urls = []
    countries = {'Spain':'ES','USA':'US', 'India':'IN', 'Japan':'JP', 'Cambodia':'KH', 'Thailand':'TH', 'United Kingdom':'GB', 'France':'FR', 'Russian Federation':'RU', 'Germany':'DE'}  # Dictionary of countries from which we get TOP 100 users (1000 users)
    for country in countries:
        start_urls.append("https://tikrank.com/influencer/influencers?page_size=100&country={}".format(countries[country]))  # link for getting user link - region (US, IN, empty[world]), count (50 or 100)
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
            yield scrapy.Request(self.userLinkBefore + item['kol_unique_id'], callback=self.get_profile_data, meta={'userLink': self.userLinkBefore + item['kol_unique_id'], 'userRegion': userRegLong})

    # Method for getting user's profile data
    def get_profile_data(self, response):
        pause(0.5)  # 0.5sec pause so we dont get timeouted from Tiktok server
        try:
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

            # Generating user media singature using nodeJS browser.js script. Script is called using Naked lib
            userMediaLink = "https://m.tiktok.com/api/item_list/?count=30&id=" + userInfo['userID'] + "&type=1&secUid=" + userInfo['userSecUid'] + "&maxCursor=0&minCursor=0&sourceType=8&appId=1233&region=CZ&language=cs&verifyFp="
            userMediaSignature = muterun_js('D:\\NodeJS\\node_modules\\tiktok-signature\\browser.js', '"' + userMediaLink + '"')   # TODO get correct absolute path to the script
            if userMediaSignature.exitcode == 0:
                # Calling method get_media_data and passing some meta data
                yield scrapy.Request(userMediaLink + "&_signature=" + userMediaSignature.stdout.decode("utf-8"), callback=self.get_media_data, meta={'userID': userInfo['userID']})
        except():
            print("Not able the get info about this user:" + response.meta['userLink'])

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
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})
process.crawl(get_data_user)
process.start()  # the script will block here until the crawling is finished
