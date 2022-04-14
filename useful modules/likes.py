import tweepy
import os
import re

proxy='http://dtiBPkKp:iX4U87RK@45.132.51.236:49044'
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'

auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_likes(USER, n_posts):
  tweet_list=api.get_favorites(screen_name = USER, count = n_posts)
  usr = tweepy.API.get_user(api, screen_name=USER)
  likes = []
  for i in tweet_list:
    likes.append({'liker' : USER, 'liker_id' : usr.id ,'liked_user' : i.user.screen_name, 'liked_user_id' : i.user.id, 'liked_post_id' : i.id, 'tweet_text' : i.text , 'tweet_hashtags' : re.findall(r'(#\w+)', i.text), 'tweet_links' : re.findall("(?P<url>https?://[^\s]+)", i.text)})
  return(likes)
