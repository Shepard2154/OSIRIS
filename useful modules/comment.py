import snscrape.modules.twitter as sntwitter
import snscrape
import time
import pandas as pd
import itertools

import tweepy
import re
import os
import json

import datetime as DT

proxy='http://dtiBPkKp:iX4U87RK@45.132.51.236:49044'
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'

#Конвертация id в screen_name и обратно
def convertation(id_or_screen_name):
  info = api.get_user(id_or_screen_name)
  if type(id_or_screen_name) == int:
    result = info.screen_name
  else:
    result = info.id_str
  return(result)

def get_api():
      auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_key, access_secret)
      api = tweepy.API(auth, wait_on_rate_limit=True)
      return api

class Comments():
  #Собирает n-твиттов пользователя, включая сделанные им ретвитты
  def get_n_tweets(USER, n_tweets):
    us = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(f'from:{USER} include:nativeretweets').get_items(), n_tweets))
    return(us)

  #Собирает комментарии к n-твиттам пользователей
  def n_comments_to_tweet(USER, n_tweet_ids):
    comment_df = pd.DataFrame()
    new_df = pd.DataFrame()
    for i in n_tweet_ids:
      comment_df = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(f'to:{USER} since_id:{i}').get_items(), n_tweet_ids)) #filter:replies
      new_df = pd.concat([new_df, comment_df], ignore_index=True)
    return(new_df)


  def get_tweet(url):
      tweet_id = url.split('/')[-1]
      api = get_api()
      tweet = api.get_status(tweet_id)
      return tweet

  

  def table(comment_urls):
    d = []
    for i in comment_urls:
      ur_twt = Comments.get_tweet(i)
      d.append({'hashtag' : re.findall(r'(#\w+)', ur_twt.text),'likes' : ur_twt.favorite_count,'retweets' : ur_twt.retweet_count})
      d_1 = pd.DataFrame(d)
    return(d_1)

#Собирает все комментарии пользователя согласно запросу
  # since - с (включительно) указанной даты по настоящий момент
  # until - до (не включительно) указанной даты
  # since-until - позволяет устанавливать промежуток
  # n_comments - n последних комментариев
  def get_comments(USER, mode):
    if mode ==  'since' or mode =='until':
      date = DT.datetime.strptime(input('Введите дату: '), '%d.%m.%Y')
      date = date.strftime('%Y-%m-%d')

    if mode == 'since':
      try:
        user_comments = pd.DataFrame(sntwitter.TwitterSearchScraper(f'from:{USER} filter:replies since:{date}').get_items())
        add = Comments.table(user_comments.url)
        all_comments = user_comments.join(add).to_dict()
      except Exception:
        print('Невозможно выдать запрос по данной дате!')
        get_comments(USER, 'since')

    elif mode == 'until':
      try:
        user_comments = pd.DataFrame(sntwitter.TwitterSearchScraper(f'from:{USER} filter:replies until:{date}').get_items())
        add = Comments.table(user_comments.url)
        all_comments = user_comments.join(add).to_dict()
      except Exception:
        print('Невозможно выдать запрос по данной дате!')
        get_comments(USER, 'until')

    elif mode == 'since-until':
      try:
        since = DT.datetime.strptime(input('Введите дату с которой хотите начать: '), '%d.%m.%Y')
        since = since.strftime('%Y-%m-%d')
        until = DT.datetime.strptime(input('Введите дату до которой хотите получить: '), '%d.%m.%Y')
        until = until.strftime('%Y-%m-%d')
        user_comments = pd.DataFrame(sntwitter.TwitterSearchScraper(f'from:{USER} filter:replies since:{since} until:{until}').get_items())
        add = Comments.table(user_comments.url)
        all_comments = user_comments.join(add).to_dict()
      except Exception:
        print('Невозможно выдать запрос по данной дате!')
        get_comments(USER, 'since-until')

    elif mode == 'n_comments':
      n_comments = int(input('Введите нужное количество комментариев:'))
      user_comments = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(f'from:{USER} filter:replies').get_items(), n_comments))
      add = Comments.table(user_comments.url)
      all_comments = user_comments.join(add).to_dict()
    return(all_comments)

# сбор комментариев к N-твиттам (включая ретвитты) пользователя
  def comments_to_dict(USER, n_tweets):
    gnt= Comments.get_n_tweets(USER, n_tweets)
    nctt = Comments.n_comments_to_tweet(USER, gnt.id)
    t = Comments.table(nctt.url)
    all = nctt.join(t).to_dict()
    return(all)
