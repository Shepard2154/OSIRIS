import nest_asyncio
import time
import sqlite3
import pandas as pd
import json
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter

from config import api

from read_write import readData, writeData
import en_core_web_sm
import tweepy
import storage
import calendar


DATABASE = "./data/osiris.db"


# Не предусмотрено, если пользователь удалил твит
def get_tweets(api, screen_name):   
    """
    Gets all new tweets from Twitter Account 
    """ 
    all_tweets = []
    lastest = storage.read_last_tweet(screen_name)[0][0]

    new_tweets = api.user_timeline(screen_name=screen_name, count=1)
    all_tweets.extend(new_tweets)
    
    if all_tweets[0].id == lastest:
        return 'all tweets up to date!'

    last = all_tweets[-1].id - 1    
    while len(new_tweets) > 0:
        print(f"getting tweets before {last}")
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=last, since_id=lastest)
        all_tweets.extend(new_tweets)
        last = all_tweets[-1].id - 1
    
    for tweet in all_tweets:
        quote_screen_name = ''
        retweete_screen_name = ''
        try:
            quote_screen_name = api.get_status(id=tweet.quoted_status_id).user.screen_name
        except Exception:
            pass

        try:
            retweete_screen_name = tweet.retweeted_status.user.screen_name
        except Exception as e:
            pass

        storage.create_tweet(tweet, quote_screen_name=quote_screen_name, retweete_screen_name=retweete_screen_name)
        
        
    print(f"...{len(all_tweets)} tweets downloaded!")



def save_tweets_csv(screen_name, tweets):
    with open(f'new_{screen_name}_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(tweets)


def get_tweet_dates(data):
    dates = {}
    for item in data:
        if dates.get(str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").date())): 
            dates[str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").date())] += 1
        else:
            dates[str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").date())] = 1
    print(dates)
    return dates


def get_tweet_time(data):
    time = {}
    for item in data:
        if time.get(str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").time())[0:2]): 
            time[str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").time())[0:2]] += 1
        else:
            time[str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").time())[0:2]] = 1
    return time


def get_tweet_weekday(data):
    weekdays = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 2, 'Thursday': 1, 'Friday': 0, 'Saturday': 0}

    for item in data:
        if weekdays.get(str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])): 
            weekdays[str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])] += 1
        else:
            weekdays[str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])] = 1
    return weekdays


def get_tweet_time_weekday(data):
    weekdays = {'Sunday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Monday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Tuesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Thursday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Friday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0], 
        'Saturday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
        }
    
    for item in data:
        if weekdays.get(str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])):
            time = str(datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").time())[0:2]
            weekdays[str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])][int(time)] += 1
        else:
            weekdays[str(calendar.day_name[datetime.strptime(item, "%Y-%m-%d %H:%M:%S%z").weekday()])] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
    return weekdays


nlp = nlp = en_core_web_sm.load()
from SimpleDecision.sentimental import Sentimental
sent = Sentimental()
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def get_sentiment(selectText):
    words = [morph.parse(word)[0].normal_form for word in re.findall(r'\w+', selectText)]
    #sentence_2 = {" ".join(words)}
    sentence = " ".join(words)
    result = sent.analyze(sentence)
    return(result)

loop = nest_asyncio.asyncio.new_event_loop()
nest_asyncio.asyncio.set_event_loop(loop)
# asyncio.new_event_loop()
nest_asyncio.apply()
# nest_asyncio.set_event_loop(loop)
# # global conn

# c_influencers = twint.Config()
# c_influencers.Store_csv = True
# c_influencers.Output = ("./data/influencers.csv")

# c_auditory = twint.Config()
# c_auditory.Store_csv = True
# c_auditory.Output = ("./data/auditory.csv")


def followersCross(ListInfluencersName, cross_count=1):
    data = readData()[ListInfluencersName]
    print(data)
    ids = []
    for item in data:
        id = api.get_user(screen_name=item).id
        ids.append(id)

    common_followers_id = storage.read_common_followers(ids, cross_count)
    return len(common_followers_id)


def followersCrossNames(ids, cross_count=1):
    start_time = time.time()

    followers = []
    common_followers_id = storage.read_common_followers(ids, cross_count)
    if len(common_followers_id) == 0:
        return ({'status_code': 404})

    count = 0

    for i in range(len(common_followers_id)):
        count += 1
        
        follower = None
        try:
            follower = api.get_user(user_id=common_followers_id[i][0])
        except tweepy.errors.TooManyRequests as e1:
            print(e1)
            time.sleep(60*15)
            follower = api.get_user(user_id=common_followers_id[i][0])
        except tweepy.errors.NotFound as e2:
            print(e2, common_followers_id[i][0])
        except tweepy.errors.TweepyException as e3:
            print(e3)
        except tweepy.errors.Forbidden as e4:
            print(e4)
        

        if follower:
            follower_info = {
                'name': follower.name,
                'screen_name': follower.screen_name,
                'statuses_count': follower.statuses_count,
                'friends_count': follower.friends_count,
                'followers_count': follower.followers_count,
                'favourites_count': follower.favourites_count,
                'listed_count': follower.listed_count,
                'profile_image_url': follower.profile_image_url,
                'description': follower.description
            }
            storage.create_follower_user(follower_info)
            followers.append(follower_info.get('screen_name'))

        print(f"{count}/{len(common_followers_id)}")
        
    print(f"--- {time.time() - start_time} seconds ---")
    return({'followersCrossNames': followers, 'status_code': 200})


def get_followers(api, users, ListInfluencersName):
    start_time = time.time()

    for user in users:
        user_id = api.get_user(screen_name=user).id
        try:
            sleeptime = 4
            pages = tweepy.Cursor(api.get_follower_ids, screen_name=user).pages()

            while True:
                try:
                    page = next(pages)
                    time.sleep(sleeptime)
                except tweepy.TooManyRequests:
                    print("Wait please! ", tweepy.TooManyRequests)
                    time.sleep(60*15) 
                    page = next(pages)
                except StopIteration:
                    print("End of work ", StopIteration)
                    break

                for follower_id in page: 
                    storage.create_follower(user_id, follower_id)

        except Exception as e:
            print("other...", e)

        print(f"--- {time.time() - start_time} seconds ---")

    try:
        writeData({ListInfluencersName: True}, name='./data/followers_count.json')
    except:
        print('no Write data')
        return ({"status_code": 404})

    return ({"status_code": 200})


# def getTwits(users,tweets_count=200,until=False,since=False):
    start_time = time.time()
    for username in users:
        if  len(since) < 6:
            until = False
        else:
            until = convertTime3(until)
            until = until + " 00:00:00"
        twint.output.clean_lists()
        c_tweets = twint.Config()
        c_tweets.Database = "./data/tweets_ca.db"
        c_tweets.Limit = tweets_count
        c_tweets.Username = username
        

        c_tweets.Until = until
        print('__--_'*20)
        print(until)
        twint.run.Search(c_tweets)
        if  len(since) < 6:
            print("NOASODOSODSOOOOOOOOOOOOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDDDDDDDDSSSSSSSSSSSSSSSSSSSSSSss")
            since = False
        else:
            print("HALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            since = convertTime3(since)
            twint.output.clean_lists()
            c_tweets = twint.Config()
            c_tweets.Database = "./data/tweets_ca.db"
            c_tweets.Limit = 10000
            c_tweets.Username = username
            #c_tweets.Until = until
            print('__--_'*20)
            print(since)
            since = since + " 00:00:00"
            # print(until)


            c_tweets.Since = since
            #c_tweets.Hide_output = True
            twint.run.Search(c_tweets)
        print(f"{username} --- {time.time() - start_time} seconds ---")
    return ({"status_code":200})


def getFollowerInfoDB(screen_name):
    data = storage.read_follower(screen_name)
    if len(data) == 0:
        return ({"status_code": 404})

    user_data = [item for item in data[0]]
    influencer = {
        'username': user_data[0], 
        'name': user_data[1], 
        'profile_image_url': user_data[2], 
        'tweets': user_data[3], 
        'following': user_data[4], 
        'followers': user_data[5],
        'likes': user_data[6],
        'media': user_data[7],
        'description': user_data[8]
        }
    
    return({"Influencer": influencer, "status_code": 200})



def getUserInfoDB(screen_name):
    data = storage.read_user(screen_name)
    if len(data) == 0:
        return ({"status_code": 404})

    user_data = [item for item in data[0]]
    influencer = {
        'username': user_data[0], 
        'name': user_data[1], 
        'profile_image_url': user_data[2], 
        'tweets': user_data[3], 
        'following': user_data[4], 
        'followers': user_data[5],
        'likes': user_data[6],
        'media': user_data[7],
        'description': user_data[8]
        }
    
    return({"Influencer": influencer, "status_code": 200})


def getInfoFromDB(screen_name):
    urls = storage.read_tweets_urls(screen_name)
    if len(urls) == 0:
        return ({"status_code": 404})
    else:
        domains = []
        for url in urls:
            domains.append(getUrlHost(url[0]))
        b = Counter(domains)
        return({"categories":sorted(b, key=b.get,reverse=True),"count":sorted(b.values(),reverse=True), "status_code":200})
    # else:
    #     sql_query = f'''select {type_}, count({type_}) as count from tweets WHERE (screen_name == "{screen_name}") and ({type_} != "")
    #                     GROUP by {type_}
    #                     ORDER BY count DESC
    #                     LIMIT 7''' 
    #     df = pd.read_sql(sql_query, conn)
    #     if len(df) == 0:
    #         return ({"status_code":404})
    #     else:
    #         return({"categories":df[type_].values.tolist(),"count":df['count'].values.tolist(),"status_code":200})

def chartHeatMapUpdate(username):
    conn = sqlite3.connect("./data/tweets_ca.db")
    sql_query = f'''select
                        si.weekday,
                        sum(case when si.hour = "00" then ct end) h0,
                        sum(case when si.hour = "01" then ct end) h1,
                        sum(case when si.hour = "02" then ct end) h2,
                        sum(case when si.hour = "03" then ct end) h3,
                        sum(case when si.hour = "04" then ct end) h4,
                        sum(case when si.hour = "05" then ct end) h5,
                        sum(case when si.hour = "06" then ct end) h6,
                        sum(case when si.hour = "07" then ct end) h7,
                        sum(case when si.hour = "08" then ct end) h8,
                        sum(case when si.hour = "09" then ct end) h9,
                        sum(case when si.hour = "10" then ct end) h10,
                        sum(case when si.hour = "11" then ct end) h11,
                        sum(case when si.hour = "12" then ct end) h12,
                        sum(case when si.hour = "13" then ct end) h13,
                        sum(case when si.hour = "14" then ct end) h14,
                        sum(case when si.hour = "15" then ct end) h15,
                        sum(case when si.hour = "16" then ct end) h16,
                        sum(case when si.hour = "17" then ct end) h17,
                        sum(case when si.hour = "18" then ct end) h18,
                        sum(case when si.hour = "19" then ct end) h19,
                        sum(case when si.hour = "20" then ct end) h20,
                        sum(case when si.hour = "21" then ct end) h21,
                        sum(case when si.hour = "22" then ct end) h22,
                        sum(case when si.hour = "23" then ct end) h23
                    from (select count(tweet) as ct, strftime("%w",datetime(rtrim(created_at,"000"), "unixepoch","localtime")) as weekday,
                        strftime("%H",datetime(rtrim(created_at,"000"), "unixepoch","localtime")) as hour
                                        from tweets where (screen_name == "{username}")
                                        GROUP by weekday, hour
                                        order by weekday, hour) si
                    group by si.weekday;'''
    df = pd.read_sql(sql_query, conn)
    if len(df) == 0:
        return ({"status_code":404})
    else:
        df.fillna(0, inplace=True)
        df = df.astype('int')
        series =[]
        for i in range(0,7):
            try:
                series.append(list(df.loc[i][1:]))
            except KeyError:
                series.append([0]*24)
        return({"heatmap":series,"status_code":200})

def getCountTwits(username):
    conn = sqlite3.connect("./data/tweets_ca.db")
    sql_query = f'''SELECT count(screen_name) as counts from tweets WHERE (screen_name == "{username}")'''
    df = pd.read_sql(sql_query, conn)
    it = df['counts'].values.tolist()[0]
    if it == 0:
        return ({"status_code":404})
    else:
        return({"countTwits":it,"status_code":200})

def charttUpdate(screen_name):
    data = storage.read_tweets_created_at(screen_name)
    all_data = []
    for item in data:
        all_data.append(item[0])

    dates = get_tweet_dates(all_data)

    if len(dates) == 0:
        return ({"status_code": 404})
    else:
        return({"charttDay": list(dates.keys()), "charttCount": list(dates.values()), "status_code": 200})

def chartWeekday(screen_name):
    data = storage.read_tweets_created_at(screen_name)
    all_data = []
    for item in data:
        all_data.append(item[0])

    weekdays = get_tweet_weekday(all_data)
    sorted_weekdays = [weekdays.get('Sunday'), weekdays.get('Monday'), weekdays.get('Tuesday'), weekdays.get('Wednesday'),
                    weekdays.get('Thursday'), weekdays.get('Friday'), weekdays.get('Saturday')] 

    if len(weekdays) == 0:
        return ({"status_code": 404})
    else:
        return({"weekdays": sorted_weekdays, "status_code": 200})

def chartHeatMap(screen_name):
    data = storage.read_tweets_created_at(screen_name)
    all_data = []
    for item in data:
        all_data.append(item[0])

    time = get_tweet_time(all_data) 
    all_time = []

    for i in range(24):
        j = str(i)
        if len(j) == 1:
            j = '0'+j
        
        result = time.get(j)
        if not result:
            result = 0
            
        all_time.append(result)

    if len(time) == 0:
        return ({"status_code": 404})
    else:
        print(all_time)
        return({"time": all_time, "status_code": 200})


def chartHeatMap2(screen_name):
    data = storage.read_tweets_created_at(screen_name)
    all_data = []
    for item in data:
        all_data.append(item[0])

    weekdays_time = get_tweet_time_weekday(all_data) 
    sorted_weekdays_time = [weekdays_time.get('Sunday'), weekdays_time.get('Monday'), weekdays_time.get('Tuesday'), weekdays_time.get('Wednesday'),
                    weekdays_time.get('Thursday'), weekdays_time.get('Friday'), weekdays_time.get('Saturday')] 

    if len(weekdays_time) == 0:
        return ({"status_code": 404})
    else:
        return({"weekdays_time": sorted_weekdays_time, "status_code": 200})


def get_lang_count(screen_name):
    data = storage.read_tweets_lang(screen_name)
    print(data)
    all_data = []
    for item in data:
        all_data.append(item[0])
    
    b = Counter(all_data)

    if len(all_data) == 0:
        return ({"status_code": 404})
    else:
        return({"langs": sorted(b, key=b.get,reverse=True), "langCount":sorted(b.values(),reverse=True), "status_code":200})
    

def get_source_count(screen_name):
    data = storage.read_tweets_source(screen_name)
    all_data = []
    for item in data:
        all_data.append(item[0])
    
    b = Counter(all_data)
    
    if len(all_data) == 0:
        return ({"status_code": 404})
    else:
        return({"sources": sorted(b, key=b.get,reverse=True), "sourceCount":sorted(b.values(),reverse=True), "status_code":200})


def extract_hashtags(hashtags):
    hashtags_with_spaces = []
    for hashtag in hashtags:
        hashtags_with_spaces.append(hashtag[0])

    hashtags_without_spaces = []
    for hashtag in hashtags_with_spaces:
        hashtags_without_spaces.extend(hashtag[:len(hashtag)-1].split(' '))
    
    hashtags_without_empty = []
    [hashtags_without_empty.append(item) for item in hashtags_without_spaces if item]

    return hashtags_without_empty 


def get_hashtags(screen_name):
    data = storage.read_tweets_hashtags(screen_name)
    hashtags = extract_hashtags(data)
    b = Counter(hashtags)
    return({"chartHashCategories": [category for category in b.keys()], "chartHashCount": [number for number in b.values()], "status_code":200})


def extract_user_mentions(user_mentions):
    user_mentions_with_spaces = []
    for user_mention in user_mentions:
        user_mentions_with_spaces.append(user_mention[0])

    user_mentions_without_spaces = []
    for user_mention in user_mentions_with_spaces:
        user_mentions_without_spaces.extend(user_mention[:len(user_mention)-1].split(' '))
    
    user_mentions_without_empty = []
    [user_mentions_without_empty.append(item) for item in user_mentions_without_spaces if item]

    return user_mentions_without_empty 


def get_user_mentions(screen_name):
    data = storage.read_tweets_user_mentions(screen_name)
    user_mentions = extract_user_mentions(data)
    b = Counter(user_mentions)
    return({"chartCashCategories": [category for category in b.keys()], "chartCashCount": [number for number in b.values()], "status_code":200})


def getTwitsToBoard(api, screen_name, created_at=datetime.now()):
    get_tweets(api, screen_name)
    tweets = storage.read_tweets(screen_name, created_at)
    all_tweets = []
    for tweet in tweets:
        all_tweets.append({"tweet": tweet[0], "date": str(datetime.strptime(tweet[1], "%Y-%m-%d %H:%M:%S%z").date()), "time": str(datetime.strptime(tweet[1], "%Y-%m-%d %H:%M:%S%z").time()), "screen_name": tweet[2], "name": tweet[3], "link": f"https://twitter.com/{tweet[2]}/status/{tweet[4]}"})
    if len(tweets) != 0:
        return({"TwitsToBoard": all_tweets, "status_code": 200})
    else:
        return({"TwitsToBoard": "Not founded tweets!", "status_code": 200})

def convertTime2(string):
    datetime_object = datetime.strptime(string, '%Y-%m-%d')
    return(datetime.strftime(datetime_object,"%d-%m-%Y"))

def convertTime3(string):
    datetime_object = datetime.strptime(string,"%d-%m-%Y")
    return(datetime.strftime(datetime_object,'%Y-%m-%d'))

def getUrlHost(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return(domain)


def getInfoAboutAccount(api, username):
    user = api.get_user(screen_name=username)

    user_info = {
        "id": user.id,
        "name": user.name,
        "screen_name": user.screen_name,
        "description": user.description,
        "location": user.location,
        "url": user.url,
        "is_protected": user.protected,
        "is_verified": user.verified,
        "followers_count": user.followers_count,
        "join_date": user.created_at.date(),
        "join_time": user.created_at.time(),
        "statuses_count": user.statuses_count,
        "friends_count": user.friends_count,
        "profile_image_url": user.profile_image_url,
        "listed_count": user.listed_count,
        "favourites_count": user.favourites_count,
        "date_update": datetime.now().date(),
        "time_update": datetime.now().time(),
    }

    storage.create_user(user_info)
    return ({"user": user_info, "status_code": 200})


def get_tweet_type_chart(screen_name):
    retweet_count = 0
    data = storage.read_tweets_type(screen_name, 'retweet_count')
    for item in data:
        retweet_count += int(item[0])

    is_quote_status = []
    data = storage.read_tweets_type(screen_name, 'is_quote_status')
    for item in data:
        is_quote_status.append(item[0])

    in_reply_to_status_id = []
    data = storage.read_tweets_type(screen_name, 'in_reply_to_status_id')
    for item in data:
        if item[0] != None:
            in_reply_to_status_id.append('True')
        else:
            in_reply_to_status_id.append('False')
    

    a2 = {'Ретвиты': retweet_count}
    b = Counter(is_quote_status)
    b2 = {'Цитаты': b.get(1)}
    d = Counter(in_reply_to_status_id)
    c2 = {'Ответы': d.get('True')}

    result = {}
    result.update(a2)
    result.update(b2)
    result.update(c2)

    return ({"typeTweet": [key for key in result.keys()], "TypeCount": [value for value in result.values()], "status_code": 200})
    

def get_tweet_quote_screen_name(screen_name):
    quote_screen_name = []
    data = storage.read_tweet_quote_screen_name(screen_name)
    for item in data:
        if item[0] != '':
            quote_screen_name.append(item[0])

    c = Counter(quote_screen_name)

    if len(quote_screen_name) != 0:
        return({"quote_screen_names": [i for i in c.keys()], "quote_screen_name_count": [i for i in c.values()], "status_code": 200})
    else:
        return({"quote_screen_names": "", "quote_screen_name_count": 0, "status_code": 200})

    
def get_tweet_retweet_screen_name(screen_name):
    retweet_screen_name = []
    data = storage.read_tweet_retweete_screen_name(screen_name)
    for item in data:
        retweet_screen_name.append(item[0])

    c = Counter(retweet_screen_name)

    if len(retweet_screen_name) != 0:
        return({"retweet_screen_names": [i for i in c.keys()], "retweet_screen_name_count": [i for i in c.values()], "status_code": 200})
    else:
        return({"retweet_screen_names": "", "retweet_screen_name_count": 0, "status_code": 200})


# getGeofenceTwits
# def getGeofenceTwits(center,radius):
    start_time = time.time()
    #for username in users:
    try:
        loop = nest_asyncio.asyncio.new_event_loop()
        nest_asyncio.asyncio.set_event_loop(loop)
        nest_asyncio.apply()
        twint.output.clean_lists()
        # nest_asyncio.apply()
        c_geo = twint.Config()
        print(type(center))
        center = center.replace("(","").replace(")","")
        c_geo.Geo = f"{center}, {radius}km"
        print(c_geo.Geo)
        c_geo.Limit = 20
        # c_geo.Store_object = True
        c_geo.Hide_output = False
        c_geo.Pandas = True
        c_geo.Lang = "en"
        c_geo.Translate = True
        c_geo.TranslateDest = "ru"
        c_geo.Pandas_clean = True  
        twint.run.Search(c_geo)
        Tweets_df = twint.storage.panda.Tweets_df
        twits = Tweets_df.T.to_dict()
        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        return ({"status_code":400})
    
    return ({"status_code":200,"twits":twits})

# def newGetTwitsEntity(users,stat_twit_count):
    start_time = time.time()
    texts = ""
    loop = nest_asyncio.asyncio.new_event_loop()
    nest_asyncio.asyncio.set_event_loop(loop)
    nest_asyncio.apply()
    print(stat_twit_count)
    for username in users:
        twint.output.clean_lists()
        c = twint.Config()
        c.Username = username
        # c.Database = "tweets.db"
        c.Pandas = True
        c.Pandas_clean = True
        c.Limit = stat_twit_count
        # c.Translate = True
        # c.TranslateDest = "en"
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        if len(Tweets_df) > 0:
            texts = texts + "\n".join(list(Tweets_df['tweet']))
    print("--- %s seconds ---" % (time.time() - start_time))
    return(getAllEntity(texts))

def getAllEntity(texts):
    texts = deEmojify(texts)
    all_entities = {}
    doc = nlp(f"{texts}")
    for ent in doc.ents:
        i = ent.label_
        if (i != 'TIME') and (i != 'DATE') and (i != 'MONEY') and (i != "ORDINAL") and (i != "CARDINAL") and (i != "QUANTITY") and (i != "PERCENT") and (i != "LANGUAGE"):
            mean = all_entities.get(ent.text)
            if mean is not None:
    #             print('not none')
                m_count = mean['count']
                m_sentences = mean['sentences']
                m_sentences_pos = mean['sentences_pos']
                m_sentences_neg = mean['sentences_neg']
                m_sentences_neutral = mean['sentences_neutral']
                m_tone_pos = mean['tone_pos']
                m_tone_neg = mean['tone_neg']
                m_tone_neutral = mean['tone_neutral']
                m_type = mean['type']
            else:
    #             print('none')
                m_count = 0
                m_sentences = []
                m_sentences_pos = []
                m_sentences_neg = []
                m_sentences_neutral = []
                m_tone_pos = 0
                m_tone_neg = 0
                m_tone_neutral = 0
                m_type = ent.label_
            m_sentences.append(ent.sent.text)
            all_entities.update({
                ent.text:{
                    "count":m_count+1,
                    "sentences":m_sentences,
                    "sentences_pos":m_sentences_pos,
                    "sentences_neg":m_sentences_neg,
                    "sentences_neutral":m_sentences_neutral,
                    "tone_pos":m_tone_pos,
                    "tone_neg":m_tone_neg,
                    "tone_neutral":m_tone_neutral,
                    "type":m_type
                }
            })
    table_data = pd.read_json(json.dumps(all_entities)).T
    table = table_data.sort_values('count',ascending=False)
    for i in range(len(table)):
        sent_pos = []
        sent_neg = []
        sent_neutral = []
        score_neg = 0
        score_pos = 0
        score_neutral = 0
        row = table.iloc[i]
        for j in row['sentences']:
            score = get_sentiment(j)['score']
            if score > 0:
                score_pos = score_pos + 1
                sent_pos.append(j)
            elif score < 0:
                score_neg = score_neg + 1
                sent_neg.append(j)
            else:
                score_neutral = score_neutral + 1
                sent_neutral.append(j)
        table.iloc[i]['tone_pos'] = score_pos
        table.iloc[i]['tone_neg'] = score_neg
        table.iloc[i]['tone_neutral'] = score_neutral
        table.iloc[i]['sentences_pos'] = sent_pos       
        table.iloc[i]['sentences_neg'] = sent_neg       
        table.iloc[i]['sentences_neutral'] = sent_neutral
#     tab = table[:50]
    table = table.sort_values('tone_pos',ascending=False)
    tone_pos = list(table['tone_pos'][:20])
    names_pos = list(table.index[:20])
    sentences_pos = list(table['sentences_pos'][:20])

    table = table.sort_values('tone_neg',ascending=False)
    tone_neg = list(table['tone_neg'][:20])
    names_neg = list(table.index[:20])
    sentences_neg = list(table['sentences_neg'][:20])

    table = table.sort_values('tone_neutral',ascending=False)
    tone_neutral = list(table['tone_neutral'][:20])
    names_neutral = list(table.index[:20])
    sentences_neutral = list(table['sentences_neutral'][:20])
#     return({"names":list(tab.index),"tone_pos":list(tab['tone_pos']),"tone_neutral":list(tab['tone_neutral']),"tone_neg":list(tab['tone_neg'])})
    out = {
        "tone_pos":tone_pos,
        "names_pos":names_pos,
        "sentences_pos":sentences_pos,

        "tone_neg":tone_neg,
        "names_neg":names_neg,
        "sentences_neg":sentences_neg,

        "tone_neutral":tone_neutral,
        "names_neutral":names_neutral,
        "sentences_neutral":sentences_neutral
    }
    names_sent_pos = {}
    for i in range(len(out['names_pos'])):
        names_sent_pos.update({out['names_pos'][i]:out['sentences_pos'][i]})
        
    names_sent_neg = {}
    for i in range(len(out['names_neg'])):
        names_sent_neg.update({out['names_neg'][i]:out['sentences_neg'][i]})
        
    names_sent_neutral = {}
    for i in range(len(out['names_neutral'])):
        names_sent_neutral.update({out['names_neutral'][i]:out['sentences_neutral'][i]})
        
    out.update({"names_sent_pos":names_sent_pos,"names_sent_neg":names_sent_neg,"names_sent_neutral":names_sent_neutral})

    return(rebuildOutput(out))

def rebuildOutput(out):
    out_pos = []
    for i in range(len(out['names_pos'])):
        if out['tone_pos'][i] != 0:
            out_pos.append({"x":out['names_pos'][i],"value":int(out['tone_pos'][i])})
        else:
            break
    out_neg = []
    for i in range(len(out['names_neg'])):
        if out['tone_neg'][i] != 0:
            out_neg.append({"x":out['names_neg'][i],"value":int(out['tone_neg'][i])})
        else:
            break
    out_neutral = []
    for i in range(len(out['names_neutral'])):
        if out['tone_neutral'][i] != 0:
            out_neutral.append({"x":out['names_neutral'][i],"value":int(out['tone_neutral'][i])})
        else:
            break
    return({"out_pos":out_pos,"out_neg":out_neg,"out_neutral":out_neutral,"out":out})

def deEmojify(inputString):
    returnString = ""
    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except:
            try:
                character.encode("cp1251")
                returnString += character
            except:
                returnString += ''
    return returnString


















# function for dowloading all followers from account with Rate Limits
#     try:
#         sleeptime = 4
#         pages = tweepy.Cursor(api.get_followers, screen_name=user).pages()
#         count = 0

#         while True:
#             try:
#                 page = next(pages)
#                 time.sleep(sleeptime)
#             except tweepy.TooManyRequests:
#                 print("Wait please! ", tweepy.TooManyRequests)
#                 time.sleep(60*15) 
#                 page = next(pages)
#             except StopIteration:
#                 print("End of work ", StopIteration)
#                 break

#             for follower in page:
#                 count += 1
#                 current_follower = api.get_user(screen_name=follower.screen_name)
#                 print(f"{count} of {user}: ", current_follower.id)

#             print("--- %s seconds ---" % (time.time() - start_time))
            
#     except Exception as e:
#         print("other...", e)