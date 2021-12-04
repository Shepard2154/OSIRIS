import tweepy

import twitter


consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


if __name__ == '__main__':
    twitter.get_last_tweets(api,'@voyage')
    twitter.get_last_tweets(api, 'wh1Co4nkIcsfUnR')
    twitter.get_last_tweets(api, 'hmfaigen')
    twitter.get_last_tweets(api, '5prings')
    twitter.get_last_tweets(api, 'computarmachine')
    twitter.get_last_tweets(api, 'techferret')
    twitter.get_last_tweets(api, 'Sony_Rus')
    twitter.get_last_tweets(api, 'dariaearlgirl')
    twitter.get_last_tweets(api, 'nastyahowell')
    twitter.get_last_tweets(api, 'melkoridze')
    twitter.get_last_tweets(api, 'ru_hp')
    twitter.get_last_tweets(api, '0xPolygon')
    twitter.get_last_tweets(api, 'vkontakte')
    twitter.get_last_tweets(api, 'KlaryMorningst1')
    twitter.get_last_tweets(api, 'joelcomm')
    twitter.get_last_tweets(api, 'PLuWex')
