import time

import tweepy

import twitter
from config import api, DATABASE
import storage


if __name__ == '__main__':
    storage.init(DATABASE)
    screen_names = ['hmfaigen', 'JacobRude']



    # request1 = twitter.get_followers(api, screen_names, 'Американские деятели')
    # print(request1)


    # request2 = twitter.get_common_followers([345762803, 51845074], 2)