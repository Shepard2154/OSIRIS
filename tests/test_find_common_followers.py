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


DATABASE = "./data/osiris.db"

if __name__ == '__main__':
    friend1 = twitter.getInfoAboutAccount(api, 'hmfaigen')
    friend2 = twitter.getInfoAboutAccount(api, 'JacobRude')


    twitter.getFollowers(api, ['hmfaigen', 'JacobRude'], 'Тест')


    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    query = f'''
        SELECT follower_id, COUNT(follower_id)
        FROM follower
        WHERE (id == {friend1.get('id')}) or (id == {friend2.get('id')})  
    '''
    cursor.execute(query)
    print(cursor.fetchall())