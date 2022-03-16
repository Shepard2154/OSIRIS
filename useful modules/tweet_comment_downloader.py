import tweepy
import re
import pandas as pd
import os
import json



#n - количесвто твиттов
def get_tweet_link(USER,n):
    IDS = []
    for tweet in tweepy.Cursor(api.user_timeline,id=USER).items(n):
        IDS.append(tweet.id)
    IDS = pd.DataFrame({'id': IDS})    
    LINKS = []
    for i in IDS.id:
        LINKS.append(get_twitter_url(USER, i))
    
    # проверка на ретвитт
    cfr = []
    for i in LINKS:
        lnk = get_tweet(i)
        try:
            lnk.retweeted_status
            cfr.append(get_twitter_url(get_tweet(i).retweeted_status.user.screen_name,get_tweet(i).retweeted_status.id))
        except AttributeError:
            cfr.append(i)
    cfr = pd.DataFrame({'link' : cfr})
    return(cfr)

# сбор юрлов комментариев
def update_urls(tweet, api, urls):
    tweet_id = tweet.id
    user_name = tweet.user.screen_name
    max_id = None
    replies = tweepy.Cursor(api.search_tweets, q='to:{}'.format(user_name),
                                since_id=tweet_id, max_id=max_id, tweet_mode='extended').items()

    for reply in replies:
        if(reply.in_reply_to_status_id == tweet_id):
            urls.append(get_twitter_url(user_name, reply.id))
            try:
                for reply_to_reply in update_urls(reply, api, urls):
                    pass
            except Exception:
                pass
        max_id = reply.id
    return urls

def get_api():
    auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def get_tweet(url):
    tweet_id = url.split('/')[-1]
    api = get_api()
    tweet = api.get_status(tweet_id)
    return tweet
    
# конструктор юрлов
def get_twitter_url(user_name, status_id):
    return "https://twitter.com/" + str(user_name) + "/status/" + str(status_id)


def table(tweet_url):
    api = get_api()
    tweet = get_tweet(tweet_url)
    urls = [tweet_url]
    urls = update_urls(tweet, api, urls)
    
    d = []
    for i in urls:
        ur_twt = get_tweet(i)
        try:
            d.append({'author': ur_twt.retweeted_status.user.screen_name, 
                  'date': ur_twt.retweeted_status.created_at, 
                  'full_text' : ur_twt.retweeted_status.text,
                  'links' : re.findall("(?P<url>https?://[^\s]+)", ur_twt.retweeted_status.text),
                  'hashtag' : re.findall(r'(#\w+)', ur_twt.retweeted_status.text),
                 'likes' : ur_twt.retweeted_status.favorite_count,
                 'retweets' : ur_twt.retweeted_status.retweet_count})
        except AttributeError:
            d.append({'author': ur_twt.user.screen_name, 
                  'date': ur_twt.created_at, 
                  'full_text' : ur_twt.text,
                  'links' : re.findall("(?P<url>https?://[^\s]+)", ur_twt.text),
                  'hashtag' : re.findall(r'(#\w+)', ur_twt.text),
                 'likes' : ur_twt.favorite_count,
                 'retweets' : ur_twt.retweet_count})

    d_1 = pd.DataFrame(d)
    return(d_1)


# ПРОВЕРИЛ НА НЭВЭЛЬНОМ, РАБОТАЕТ КАК НАДО)    
USER = 'navalny'
n=2  
  
#получаем ссылки на n твиттов (если ретвит, то ссылка на его оригинал)
gtl = get_tweet_link(USER, n)
print(gtl)

# сохранение таблиц в json
for i, j in zip(gtl.link, range(len(gtl.link))):
    table(i).to_json(f'table_{j + 1}.json')

input('Press F to pay RESPECT')