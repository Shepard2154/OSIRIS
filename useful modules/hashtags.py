import os
import re
import time

import tweepy
from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_KEY'), os.getenv('ACCESS_SECRET'))
api = tweepy.API(auth)

proxy = os.getenv('PROXY')

options = {
    'proxy': {
        'http': proxy,
        'https': proxy
    }
} 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options, chrome_options=chrome_options)

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


def get_some_tweets(query):
    some_tweets = []

    wd.get('https://twitter.com/search?q=%23'+query+'&src=typed_query')
    time.sleep(10)

    raw_tweets = wd.find_elements(by=By.XPATH, value="//article[@role='article']")
    print('count of tweets: ', len(raw_tweets))
    for raw_tweet in raw_tweets:
        # screen_name = raw_tweet.find_element(by=By.XPATH, value=".//following::span[contains(.,'@')]").get_attribute('innerHTML')
        # created_at = raw_tweet.find_element(by=By.XPATH, value=".//following::time").get_attribute('datetime')
        status_link = raw_tweet.find_element(by=By.XPATH, value=".//following::time/parent::*").get_attribute('href')

        status_id_pattern = r"status\/(\d+)"
        status_id = re.search(status_id_pattern, status_link).group(1)

        tweet = api.get_status(id=status_id)
        some_tweets.append(tweet._json)
    return some_tweets

some_tweets = get_some_tweets('cb')
print(some_tweets, len(some_tweets))