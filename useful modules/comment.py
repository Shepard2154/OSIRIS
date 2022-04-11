import snscrape.modules.twitter as sntwitter
import snscrape
import time
import pandas as pd
import itertools

import tweepy
import re
import os
import json

proxy='http://dtiBPkKp:iX4U87RK@45.132.51.236:49044'
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'

class Comments():
  def get_n_tweets(USER, n_tweets):
    us = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(f'from:{USER} include:nativeretweets').get_items(), n_tweets))
    return(us)


  def n_comments_to_tweet(USER, n_tweet_ids):
    comment_df = pd.DataFrame()
    new_df = pd.DataFrame()
    for i in n_tweet_ids:
      comment_df = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(f'to:{USER} since_id:{i}').get_items(), 100)) #filter:replies
      new_df = pd.concat([new_df, comment_df], ignore_index=True)
    return(new_df)


  def get_tweet(url):
      tweet_id = url.split('/')[-1]
      api = get_api()
      tweet = api.get_status(tweet_id)
      return tweet

  def get_api():
      auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_key, access_secret)
      api = tweepy.API(auth, wait_on_rate_limit=True)
      return api

  def table(comment_urls):
    d = []
    for i in comment_urls:
      ur_twt = get_tweet(i)
      d.append({'hashtag' : re.findall(r'(#\w+)', ur_twt.text),'likes' : ur_twt.favorite_count,'retweets' : ur_twt.retweet_count})
      d_1 = pd.DataFrame(d)
    return(d_1)

# сбор N-твиттов включая ретвитты
USER = input('Введите имя ')
n_tweets = int(input('Введите количество твиттов '))
def comments_to_dict(USER, n_tweets):
  gnt= Comments.get_n_tweets(USER, n_tweets)
  nctt = Comments.n_comments_to_tweet(USER, gnt.id)
  t = Comments.table(nctt.url)
  all = nctt.join(t).to_dict()
  return(all)
  
p = comments_to_dict(USER, n_tweets)
print(p)  