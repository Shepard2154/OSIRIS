import os
import re

import tweepy
from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
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

browser = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options, chrome_options=chrome_options)

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


def getting_tweets_by_hashtag(hashtag_value):
    browser.get('https://twitter.com/search?q=%23'+hashtag_value+'&src=typed_query&f=live')
    WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_all_elements_located((By.XPATH, "//article[@role='article']"))) 

    while True:
        raw_tweets = browser.find_elements(by=By.XPATH, value="//article[@role='article']")
        print('\ncount of tweets: ', len(raw_tweets))
        for raw_tweet in raw_tweets:
            status_link = raw_tweet.find_element(by=By.XPATH, value=".//following::time/parent::*").get_attribute('href')

            status_id_pattern = r"status\/(\d+)"
            status_id = re.search(status_id_pattern, status_link).group(1)

            tweet = api.get_status(id=status_id)
            yield tweet._json
        
        browser.execute_script("arguments[0].scrollIntoView();", raw_tweets[-1])
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))


for tweet in getting_tweets_by_hashtag('cb'):
    print(tweet.get('user').get('screen_name'), tweet.get('id'))


