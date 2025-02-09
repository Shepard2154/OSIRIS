import datetime
import sqlite3

import getters
from config import TWITTER_DB

def init():
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS
            user(
                id integer not null,
                screen_name text not null,
                name text default '',
                description text default '',
                location text default '',
                url text default '',
                join_date text not null,
                join_time text not null,
                statuses_count integer default 0,
                friends_count integer default 0,
                followers_count integer default 0,
                favourites_count integer default 0,
                listed_count integer default 0,
                is_protected bool not null,
                is_verified bool not null,
                profile_image_url text default '',
                date_update text not null,
                time_update text not null,
                CONSTRAINT users_pk PRIMARY KEY (id)
            );
        """
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS
            tweet (
                id integer not null,
                text text default '',
                truncated bool not null,
                created_at text not null,
                lang text default '',
                retweet_count integer default 0,
                favorite_count_count integer default 0,
                hashtags text default '',
                urls text default '',
                user_mentions text default '',
                place text default '',
                coordinates text default '',
                user_id integer not null,
                screen_name text not null,
                name text default '',
                source text default '',
                in_reply_to_status_id text default '',
                in_reply_to_user_id text default '',
                in_reply_to_screen_name text default '',   
                is_quote_status bool default False,
                retweeted bool default False,
                media text default '',
                quote_screen_name text default '',
                retweete_screen_name text default '',
                PRIMARY KEY (id)
            );
    """
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS
            follower (
                id integer not null,
                follower_id integer not null,
                CONSTRAINT follower_pk PRIMARY KEY (id, follower_id),
                CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES user(id),
                CONSTRAINT follower_id_fk FOREIGN KEY(follower_id) REFERENCES user(id)
            );
    """
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS
            follower_user (
                user_ids text not null,
                follower_id integer not null,
                screen_name text not null,
                name text default '',
                profile_image_url text default '',
                statuses_count integer default 0,
                friends_count integer default 0,
                followers_count integer default 0,
                favourites_count integer default 0,
                listed_count integer default 0,
                description text default '',
                CONSTRAINT users_pk PRIMARY KEY (screen_name)
            );
    """ 

    query = """
    CREATE TABLE IF NOT EXISTS
            geofencing (
                id integer not null,
                text text default '',
                date text not null,
                link text default '',
                translate text default '',
                nlikes integer not null,
                place text default '',
                nretweets integer not null,
                nreplies integer not null,
                retweet bool not null,
                hashtags text default '',
                username text default '',
                name text default '',
                CONSTRAINT geo_pk PRIMARY KEY (id)
            );
    """

    cursor.execute(query)
    connection.commit()
    return 1


def create_user(user):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f"""
        INSERT OR REPLACE INTO user 
        VALUES (
            {user.get('id')},
            "{user.get('screen_name')}",
            "{user.get('name').replace('"', '')}",
            "{str(user.get('description')).replace('"', "'")}",
            "{str(user.get('location')).replace('"', '')}",
            "{str(user.get('url')).replace('"', '')}",
            '{user.get('join_date')}',
            '{user.get('join_time')}',
            {user.get('statuses_count')},
            {user.get('friends_count')},
            {user.get('followers_count')},
            {user.get('favourites_count')},
            {user.get('listed_count')},
            {user.get('is_protected')},
            {user.get('is_verified')},
            '{user.get('profile_image_url')}',
            '{user.get('date_update')}',
            '{user.get('time_update')}'
        )
    """
    cursor.execute(query)
    connection.commit()


def create_geotweet(tweet):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f"""
        INSERT OR REPLACE INTO geofencing 
        VALUES (
            {tweet.get('id')},
            "{tweet.get('text').replace('"', "'")}",
            "{tweet.get('date').replace('"', "'")}",
            "{tweet.get('link').replace('"', "'")}",
            "{tweet.get('translate').replace('"', "'")}",
            {tweet.get('nlikes')},
            "{tweet.get('place').replace('"', "'")}",
            {tweet.get('nretweets')},
            {tweet.get('nreplies')},
            "{tweet.get('retweet')}",
            "{tweet.get('hashtags')}",
            "{tweet.get('username').replace('"', '')}",
            "{tweet.get('name').replace('"', "'")}"
            )
    """
    print(query)
    cursor.execute(query)
    connection.commit()


def create_follower_user(follower_user):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f"""
        INSERT OR REPLACE INTO follower_user 
        VALUES (
            "{follower_user.get('screen_name')}",
            "{follower_user.get('name').replace('"', "'")}",
            '{follower_user.get('profile_image_url')}',
            {follower_user.get('statuses_count')},
            {follower_user.get('friends_count')},
            {follower_user.get('followers_count')},
            {follower_user.get('favourites_count')},
            {follower_user.get('listed_count')},
            "{str(follower_user.get('description')).replace('"', "'")}"           
        )
    """
    print(query)
    cursor.execute(query)
    connection.commit()
    


def read_user(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT screen_name, name, profile_image_url, statuses_count, friends_count, followers_count, favourites_count, listed_count, description 
        FROM user 
        WHERE screen_name == "{screen_name}"
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_follower(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT screen_name, name, profile_image_url, statuses_count, friends_count, followers_count, favourites_count, listed_count, description 
        FROM follower_user 
        WHERE screen_name == "{screen_name}"
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_all_followers():
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT screen_name, name, profile_image_url, statuses_count, friends_count, followers_count, favourites_count, listed_count, description 
        FROM follower_user
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data

# Вот эту функцию нужно конкретно тестировать
def create_tweet(tweet, quote_screen_name='', retweete_screen_name=''):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    try:
        place = tweet.place.url
        coordinates = tweet.coordinates.get('coordinates')
    except Exception:
        place = ''
        coordinates = ''

    query = f"""
            INSERT or REPLACE INTO tweet 
            VALUES (
                {tweet.id},
                "{tweet.full_text.replace('"', '')}",
                {tweet.truncated},
                '{tweet.created_at}',
                '{tweet.lang}',
                {tweet.retweet_count},
                {tweet.favorite_count},
                "{str(getters.get_hashtags(tweet)).replace('"', '')}",
                "{str(getters.get_urls(tweet)).replace('"', '')}",
                "{str(getters.get_user_mentions(tweet)).replace('"', '')}",
                "{place}", 
                "{coordinates}",
                {tweet.user.id},
                '{tweet.user.screen_name}',
                "{tweet.user.name.replace('"', '')}",
                '{tweet.source}',
                '{tweet.in_reply_to_status_id}',
                '{tweet.in_reply_to_user_id}' ,
                '{tweet.in_reply_to_screen_name}',   
                {tweet.is_quote_status},
                '{tweet.retweeted}',
                "{str(getters.get_media_url(tweet)).replace('"', '')}",
                '{quote_screen_name}',
                '{retweete_screen_name}'
            )
        """
    cursor.execute(query)
    connection.commit()


def read_last_tweet(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f"""
    SELECT MIN(id) FROM tweet WHERE screen_name='{screen_name}'
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets(screen_name, created_at=datetime.datetime.now()):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f"""
        SELECT text, created_at, screen_name, name, id 
        FROM tweet 
        WHERE ((screen_name == "{screen_name}") AND (created_at < "{created_at}"))
        ORDER BY created_at 
        DESC
        LIMIT 12
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_urls(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f"""
        SELECT urls 
        FROM tweet 
        WHERE (screen_name == "{screen_name}") and (urls != "")
    """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_created_at(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT created_at 
        FROM tweet where (screen_name == "{screen_name}")
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_lang(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT lang
        FROM tweet
        WHERE (screen_name == "{screen_name}")
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_source(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT source
        FROM tweet
        WHERE (screen_name == "{screen_name}")
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_hashtags(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT hashtags
        FROM tweet
        WHERE (screen_name == "{screen_name}")
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_user_mentions(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT user_mentions
        FROM tweet
        WHERE (screen_name == "{screen_name}") 
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweets_type(screen_name, type):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
    SELECT {type}  
    FROM tweet
    WHERE screen_name = '{screen_name}'
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweet_count(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
    SELECT COUNT(*)
    FROM tweet
    WHERE screen_name='{screen_name}'
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweet_quote_screen_name(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
    SELECT quote_screen_name
    FROM tweet
    WHERE screen_name='{screen_name}'
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweet_retweete_screen_name(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
    SELECT retweete_screen_name
    FROM tweet
    WHERE (retweete_screen_name != '') AND
    (screen_name='{screen_name}')
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data
        

def create_follower_name(screen_name, follower_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()

    time_update = datetime.datetime.now()

    query = f'''
    INSERT or REPLACE INTO followers_names
    VALUES (
        "{screen_name}", 
        "{follower_name.replace('"', '')}", 
        "{time_update}")
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def create_follower(user_id, follower_id):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()

    query = f'''
    INSERT or REPLACE INTO follower
    VALUES (
        {user_id}, 
        {follower_id}
        )
    '''
    cursor.execute(query)
    connection.commit()


def read_common_followers(ids: list, cross_count: int):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()

    ids = tuple(ids)
    if len(ids) == 1:
        ids = str(ids).replace(',', '')

    query = f'''
        SELECT follower_id
        FROM (
            SELECT follower_id, COUNT(follower_id) as quontity
            FROM follower
            WHERE id IN {ids}
            GROUP BY follower_id
        )
        WHERE quontity = {cross_count}
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_tweet_text(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT text
        FROM tweet
        WHERE screen_name = "{screen_name}"
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data

def read_tweets_count(screen_name):
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT COUNT(*) 
        FROM tweet
        WHERE screen_name = "{screen_name}"
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def read_all_geotweets():
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        SELECT * 
        FROM geofencing
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.commit()
    return data


def delete_all_geotweets():
    connection = sqlite3.connect(TWITTER_DB)
    cursor = connection.cursor()
    query = f'''
        DELETE FROM geofencing
    '''
    cursor.execute(query)
    connection.commit()