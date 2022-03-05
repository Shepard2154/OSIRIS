import os
import re

import tweepy
from loguru import logger
from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

logger.add("main.log", format="{time}  {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

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

driver = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options, chrome_options=chrome_options)

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


@logger.catch
def getting_tweets_by_hashtag(hashtag_value):
    driver.get('https://twitter.com/search?q=%23'+hashtag_value+'&src=typed_query&f=live')
    
    while True:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, "//article[@role='article']"))) 

        tweets_elements = driver.find_elements(by=By.XPATH, value="//article[@role='article']//following::time/parent::*")
        tweets_links = list(filter(None, [element.get_attribute('href') for element in tweets_elements]))

        logger.debug(f"count of tweets: {len(tweets_links)}")
        for link in tweets_links: 
            tweet_id_pattern = r"status\/(\d+)"
            tweet_id = re.search(tweet_id_pattern, link).group(1)

            tweet = api.get_status(id=tweet_id)
            yield tweet._json

        scroll_to(tweets_elements[-1])        


def scroll_to(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


if __name__ == 'main':
    for tweet in getting_tweets_by_hashtag('cb'):
        print(tweet.get('user').get('screen_name'), tweet.get('id'))

