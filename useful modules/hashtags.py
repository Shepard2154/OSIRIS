import collections
import os
import re
import time

import tweepy
from loguru import logger
from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

logger.add("hashtags.log", format="{time}  {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

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


class TweetsMemory(list):
    tweets_id = collections.deque()
    used_to = 0

    def add(self, id):
        if id not in self.tweets_id:
            self.used_to += 1
            self.tweets_id.append(id)

    def reduce(self):
        if len(self.tweets_id) > 20:
            self.tweets_id.popleft()
    
    def exists(self, id):
        if id in self.tweets_id:
            return True
        else:
            return False

    def values(self):
        return self.tweets_id

    def length(self):
        return len(self.tweets_id)


memory = TweetsMemory()


@logger.catch
def getting_tweets_by_hashtag(hashtag_value):
    driver.get('https://twitter.com/search?q=%23'+hashtag_value+'&src=typed_query&f=live')
    
    while True:
        WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, "//article[@role='article']"))) 

        tweets_elements = driver.find_elements(by=By.XPATH, value="//article[@role='article']//following::time/parent::*")
        tweets_links = list(filter(None, [element.get_attribute('href') for element in tweets_elements]))

        for link in tweets_links: 
            tweet_id_pattern = r"status\/(\d+)"
            tweet_id = re.search(tweet_id_pattern, link).group(1)

            try:
                tweet = api.get_status(id=tweet_id)
            except tweepy.errors.TooManyRequests:
                logger.warning(f"Too many requests. Wait 15 minutes!")
                logger.info(f"{memory.used_to} tweets were downloaded!")
                
                time.sleep(60*15)
                tweet = api.get_status(id=tweet_id)

            if memory.exists(tweet._json.get('id')):
                continue
            else:
                memory.add(tweet._json.get('id'))
                memory.reduce()
                yield tweet._json

        scroll_to(tweets_elements[-1])        


def scroll_to(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


if __name__ == '__main__':
    tweets_id = []
    start_time = time.time()
    for tweet in getting_tweets_by_hashtag('cb'):
        tweets_id.append(tweet.get('id'))
        logger.debug(f"{tweet.get('user').get('screen_name')} - {tweet.get('id')}")

        # if time.time() - start_time >= 30:
        #     break
    
    logger.info(f"{memory.used_to} tweets were downloaded!")
