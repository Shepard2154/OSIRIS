import sqlite3
import tweepy
import twitter

import storage

consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':
    storage.init()
    req = twitter.getInfoAboutAccount(api, 'wh1Co4nkIcsfUnR')
    req = twitter.getInfoAboutAccount(api, 'hmfaigen')
    req = twitter.getInfoAboutAccount(api, '5prings')
    req = twitter.getInfoAboutAccount(api, 'computarmachine')
    req = twitter.getInfoAboutAccount(api, 'techferret')
    req = twitter.getInfoAboutAccount(api, 'Sony_Rus')
    req = twitter.getInfoAboutAccount(api, 'dariaearlgirl')
    req = twitter.getInfoAboutAccount(api, 'nastyahowell')
    req = twitter.getInfoAboutAccount(api, 'melkoridze')
    req = twitter.getInfoAboutAccount(api, 'ru_hp')
    req = twitter.getInfoAboutAccount(api, '0xPolygon')
    req = twitter.getInfoAboutAccount(api, 'vkontakte')
    req = twitter.getInfoAboutAccount(api, 'KlaryMorningst1')
    req = twitter.getInfoAboutAccount(api, 'joelcomm')
    req = twitter.getInfoAboutAccount(api, 'PLuWex')
