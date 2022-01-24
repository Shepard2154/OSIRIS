import datetime as dt
import logging
import os
import subprocess
import time
from datetime import datetime

import flask
import flask_login
import json_log_formatter
from dotenv import load_dotenv
from flask import (
    json,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
)
from flask_cors import CORS

import storage
import twitter
from config import api
from read_write import readData, writeData
from twitter import (
    charttUpdate,
    followersCross,
    followersCrossNames,
    get_all_tweets,
    getGeofenceTwits,
    getInfoAboutAccount,
    getInfoFromDB,
    getTwitsToBoard,
    getUserInfoDB,
    newGetTwitsEntity,
    get_followers,
)


load_dotenv()


app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app)


storage.init()


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('./data/app.json')
formatter = json_log_formatter.JSONFormatter()
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()

def set_logger(logger):
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = set_logger(logger)


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(login):
    user = User()
    user.id = login
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("/login/")


@app.route('/logout/',methods=['GET','POST','OPTIONS'])
def logout():
    flask_login.logout_user()
    return redirect("/login/")


@app.route("/login/",methods=['GET','POST','OPTIONS'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    req = json.loads(request.data.decode('utf-8'))
    login = req['login']
    password = req['password']
    users = ['useruser','user1','user2']

    if (login in users) and (password == "test"):
        user = User()
        user.id = login
        flask_login.login_user(user)
        return make_response(jsonify('Authorized'), 200)
    else:
        return make_response(jsonify('Unauthorized'), 401)


@app.route("/",methods=['POST','OPTIONS','GET'])
@flask_login.login_required
def getDocuments():
    return render_template('index.html')


@app.route("/ca/",methods=['POST','OPTIONS','GET'])
@flask_login.login_required
def getCa():
    list_influencers = list(readData().keys())
    return render_template('ca.html', list_influencers=list_influencers)


@app.route("/analitica/",methods=['POST','OPTIONS','GET'])
@flask_login.login_required
def getAnalitica():
    try:
        ca_categories = readData(name='./data/ca.json').keys()
    except:
        ca_categories = ''
        ca_categories = ''
    return render_template('analitica.html', CaListNames=ca_categories)


@app.route("/geofence/",methods=['POST','OPTIONS','GET'])
@flask_login.login_required
def getGeofence():
    return render_template('geofence.html')


@app.route("/infopovod/",methods=['POST','OPTIONS','GET'])
@flask_login.login_required
def getInfopovod():
    return render_template('infopovod.html')


@app.route("/getInfoAboutTwitterAccountName/",methods=['POST','OPTIONS','GET'])
def getInfoAboutTwitterAccountName():
    user_info = {
                "status":"okey",
                "accountName":"",
                "chartAnswersCategories":[],
                "chartAnswersCount":[], 
                "heatmap":[[0],[0],[0],[0],[0],[0],[0]],
                "countTwits":0,
                "charttDay":[False],
                "charttCount":[False],
                "chartHashCategories":[],
                "chartHashCount":[],
                "chartCashCategories":[],
                "chartCashCount":[],
                "chartUrlCategories":[],
                "chartUrlCount":[],
                "TwitsToBoard":[]
            }
    try:
        twitterAccountName = json.loads(request.data.decode('utf-8'))['accountName']
    except:
        logger.error('"_status_code": 422, "error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}), 422)

    account = getInfoAboutAccount(api, twitterAccountName)
    
    if account['status_code'] != 200:
        logger.error({"error": "accountName is not found"})
        return make_response(jsonify({"_status_code": 422, "error":"accountName is not found"}), 422)
    else:
        twitter.get_last_tweets(api, account['user']['screen_name'])

        twitterAccountName = account['user']['screen_name']
        user_info.update({"accountName": account['user']['name']})
        user_info.update({"screen_name": account['user']['screen_name']})
        user_info.update({"count_tweets_in_db": storage.read_tweets_count(twitterAccountName)})
        user_info.update({"countTwits": account['user']['statuses_count']})
        user_info.update({"location": account['user']['location']})
        user_info.update({"description": account['user']['description']})
        user_info.update({"join_date": account['user']['join_date']})
        user_info.update({"likes": account['user']['favourites_count']})
        user_info.update({"profile_image_url": account['user']['profile_image_url']})
        user_info.update({"following": account['user']['friends_count']})
        user_info.update({"followers": account['user']['followers_count']})
        user_info.update({"id": account['user']['id']})
        user_info.update({"media": account['user']['listed_count']})
        user_info.update({"tweets": account['user']['statuses_count']})

        weekdays = twitter.chartWeekday(twitterAccountName)
        if weekdays['status_code'] == 200:
            user_info.update({"weekdays": weekdays['weekdays']})

        weekdays_time = twitter.chartHeatMap(twitterAccountName)
        if weekdays_time['status_code'] == 200:
            user_info.update({"weekdays_time": weekdays_time['weekdays_time']}) 
        
        langs = twitter.get_lang_count(twitterAccountName)
        if langs['status_code'] == 200:
            user_info.update({"langs": langs['langs'], "langCount": langs["langCount"]})

        sources = twitter.get_source_count(twitterAccountName)
        if sources['status_code'] == 200:
            user_info.update({"sources": sources['sources'], "sourceCount": sources["sourceCount"]})

        TwitsToBoard = getTwitsToBoard(api, twitterAccountName)
        if TwitsToBoard['status_code'] == 200:
            user_info.update({"TwitsToBoard": TwitsToBoard['TwitsToBoard']})

        chartUrl = getInfoFromDB(twitterAccountName)
        if chartUrl['status_code'] == 200:
            user_info.update({"chartUrlCategories": chartUrl['categories'][:7], "chartUrlCount":chartUrl['count'][:7]})
        
        chartHash = twitter.get_hashtags(twitterAccountName)
        if chartHash['status_code'] == 200:
            user_info.update({"chartHashCategories": chartHash['chartHashCategories'], "chartHashCount":chartHash['chartHashCount']})
        
        chartCash = twitter.get_user_mentions(twitterAccountName)
        if chartCash['status_code'] == 200:
            user_info.update({"chartCashCategories": chartCash['chartCashCategories'], "chartCashCount":chartCash['chartCashCount']})

        chartt = charttUpdate(twitterAccountName)
        if chartt['status_code'] == 200:
            user_info.update({"charttDay": chartt['charttDay'], "charttCount": chartt['charttCount']})

        tweet_type = twitter.get_tweet_type_chart(twitterAccountName)
        if tweet_type['status_code'] == 200:
            user_info.update({"typeTweet": tweet_type['typeTweet'], "TypeCount": tweet_type["TypeCount"]})

        quotes_screen_name = twitter.get_tweet_quote_screen_name(twitterAccountName)
        if quotes_screen_name['status_code'] == 200:
            user_info.update({"quote_screen_names": quotes_screen_name['quote_screen_names'], "quote_screen_name_count": quotes_screen_name["quote_screen_name_count"]})

        retweet_screen_names = twitter.get_tweet_retweet_screen_name(twitterAccountName)
        if quotes_screen_name['status_code'] == 200:
            user_info.update({"retweet_screen_names": retweet_screen_names['retweet_screen_names'], "retweet_screen_name_count": retweet_screen_names["retweet_screen_name_count"]})   
        return make_response(jsonify(user_info), 200)


# infopovod page (нажатие на кнопку "Загрузить еще")
@app.route('/addDopMessage/',methods=['POST','OPTIONS','GET'])
def addDopMessage():
    try:
        twitterAccountName = json.loads(request.data.decode('utf-8'))['accountName']
        created_at = json.loads(request.data.decode('utf-8'))['created_at']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    if not created_at:
        created_at = datetime.now()

    TwitsToBoard = getTwitsToBoard(api, twitterAccountName, created_at)

    if TwitsToBoard['status_code'] != 200:
        logger.error({"error": "TwitsToBoard not found"})
        return make_response(jsonify({"_status_code":404,"error":"TwitsToBoard not found"}),404)
    else:
        return make_response(jsonify({"TwitsToBoard":TwitsToBoard['TwitsToBoard'],"status_code":200}),200)


@app.route('/addDopPerson/', methods=['POST','OPTIONS','GET'])
def addDopPerson():
    try:
        twitterAccountName = json.loads(request.data.decode('utf-8'))['accountName']
        number = json.loads(request.data.decode('utf-8'))['created_at']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    if not created_at:
        created_at = datetime.now()

    TwitsToBoard = getTwitsToBoard(api, twitterAccountName, created_at)

    if TwitsToBoard['status_code'] != 200:
        logger.error({"error": "TwitsToBoard not found"})
        return make_response(jsonify({"_status_code":404,"error":"TwitsToBoard not found"}),404)
    else:
        return make_response(jsonify({"TwitsToBoard":TwitsToBoard['TwitsToBoard'],"status_code":200}),200)


@app.route('/getTwits/',methods=['POST','OPTIONS','GET'])
def getTwitss():
    try:
        twitterAccountName = json.loads(request.data.decode('utf-8'))['accountName']
        until = json.loads(request.data.decode('utf-8'))['until']
        print(f"+++++++++++++++++++++++++++{until}++++++++++++++++++++++++++++")
        since = json.loads(request.data.decode('utf-8'))['since']
        print(f"+++++++++++++++++++++++++++{since}++++++++++++++++++++++++++++")
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    twits = twitter.get_all_tweets(api, twitterAccountName, since, until)
    if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code": 404, "error": "Twits not found"}), 404)
    else:
        return make_response(jsonify({"status_code": 200}), 200)


@app.route('/addNewListInfluencers/',methods=['POST','OPTIONS','GET'])
def addNewListInfluencers():
    try:
        NewListInfluencersName = json.loads(request.data.decode('utf-8'))['NewListInfluencersName']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    status = writeData({NewListInfluencersName:[]})
    print(status)
    #data = readData()
    #print(data)
    ListsInfluencers =list(readData().keys())
    if False:# if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
        return make_response(jsonify({"status_code":200,"ListsInfluencers":ListsInfluencers}),200)


@app.route('/ListInfluencers/',methods=['POST','OPTIONS','GET'])
def ListInfluencers():
    try:
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
    except:
        logger.error('"_status_code": 422, "error": ["info": "incorrect POST-request"]')
        return make_response(jsonify({"_status_code": 422, "error": {"info": "incorrect POST-request"}}), 422)

    data = readData()[ListInfluencersName]
    print(data)

    Influencers = []
    if len(data) != 0:
        for user in data:
            req = getUserInfoDB(user)
            print(req)
            if req['status_code'] == 200:
                Influencers.append(req['Influencer'])
    try:
        data2 = readData(name='followers_count.json')[ListInfluencersName]
    except:
        data2 = False
    return make_response(jsonify({"status_code":200,"Influencers":Influencers,"Followers":data2}),200)


@app.route('/addUserToList/',methods=['POST','OPTIONS','GET'])
def addUserToList():
    try:
        accountName = json.loads(request.data.decode('utf-8'))['accountName']
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    data = readData()[ListInfluencersName]
    if accountName not in data:
        account = getInfoAboutAccount(api, accountName)
        if account['status_code'] != 200:
            logger.error({"error": "accountName not found"})
            return make_response(jsonify({"_status_code": 422, "error": "accountName not found"}), 422)
        else:
            data.append(account['user']['screen_name'])
            writeData({ListInfluencersName: data})
            account['user']['date_update'] = str(account['user']['date_update'])    
            account['user']['time_update'] = str(account['user']['time_update'])
            account['user']['join_time'] = str(account['user']['join_time'])   
        return make_response(jsonify({"status_code": 200, "Influencer": account['user']}), 200)
    else:
        return make_response(jsonify({"_status_code": 404, "error": "User already exists!"}), 404)


@app.route('/removeUserFromList/',methods=['POST','OPTIONS','GET'])
def removeUserFromList():
    try:
        accountName = json.loads(request.data.decode('utf-8'))['accountName']
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    data = readData()[ListInfluencersName]
    if accountName in data:
        data.remove(accountName)
        writeData({ListInfluencersName:data})
        if False:# if twits['status_code'] != 200:
            logger.error({"error": "Twits not found"})
            return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
        else:
            return make_response(jsonify({"status_code":200}),200)
    else:
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)

@app.route('/downloadFollowers/',methods=['POST','OPTIONS','GET'])
def downloadFollowers():
    try:
        start_time = time.time()
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
    except:
        logger.error('"_status_code": 422, "error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code": 422, "error": {"info":"incorrect POST-request"}}), 422)

    data = readData()[ListInfluencersName]

    if len(data) != 0:
        result = get_followers(api, data, ListInfluencersName)
        if result['status_code'] != 200:
            logger.error({"error": "result not found"})
            return make_response(jsonify({"_status_code": 422, "error": "accountName not found"}), 422)
        else:
            print(f"app.py downloadFollowers--- {time.time() - start_time} seconds ---")
            return make_response(jsonify({"status_code": 200}), 200)
    else:
        return make_response(jsonify({"_status_code": 404, "error": "Twits not found"}), 404)

 

@app.route('/downloadFullFollowers/',methods=['POST','OPTIONS','GET'])
def downloadFullFollowers():
    try:
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
        cross_count = json.loads(request.data.decode('utf-8'))['crossCount']
        start_person = json.loads(request.data.decode('utf-8'))['start_person']
        end_person = json.loads(request.data.decode('utf-8'))['end_person']

        print(start_person, end_person)
    except:
        logger.error('"_status_code": 422, "error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code": 422, "error": {"info": "incorrect POST-request"}}), 422)

    data = readData()[ListInfluencersName]
    print(data)

    if len(data) != 0:
        ids = []
        for item in data:
            id = api.get_user(screen_name=item).id
            ids.append(id)

        result = followersCrossNames(ids, start_person, end_person, cross_count)
        if result['status_code'] != 200:
            logger.error({"error": "result not found"})
            return make_response(jsonify({"_status_code": 422, "error": "accountName not found"}),422)
        else:
            followersCrossNamess = result['followersCrossNames']
            if len(followersCrossNamess) != 0:
                return make_response(jsonify({"status_code": 200, "ListInfluencersNames": followersCrossNamess}),200)
            else:
                return make_response(jsonify({"_status_code": 404, "error": "Followers don't exist"}), 404)

    else:
        return make_response(jsonify({"_status_code": 404, "error": "There are not users"}), 404)


@app.route('/uploadGeoTweets/', methods=['POST', 'OPTIONS', 'GET'])
def uploadGeoTweets():
    try:
        start_tweet = json.loads(request.data.decode('utf-8'))['start_tweet']
        end_tweet = json.loads(request.data.decode('utf-8'))['end_tweet']

        print('app.py uploadGeoTweets()', start_tweet, end_tweet)
    except:
        logger.error('"_status_code": 422, "error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code": 422, "error": {"info": "incorrect POST-request"}}), 422)

    geo_tweets = twitter.getGeoTweets(start_tweet, end_tweet)

    if geo_tweets['status_code'] != 200:
            logger.error({"error": "result not found"})
            return make_response(jsonify({"_status_code": 422, "error": "geotweets did not find"}), 422)
    else: 
        if len(geo_tweets.get('twits')) != 0:
            return  make_response(jsonify({"_status_code": 200, "twits": geo_tweets.get('twits')}), 200)
        else:
            return make_response(jsonify({"_status_code": 404, "error": "There are not geotweets"}), 404)


@app.route('/statTimeUpdate/',methods=['POST','OPTIONS','GET'])
def statTimeUpdate():
    try:
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
        cross_count = json.loads(request.data.decode('utf-8'))['cross_count']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    result = followersCross(ListInfluencersName, cross_count)
    # if result['status_code'] != 200:
    #     logger.error({"error": "result not found"})
    #     return make_response(jsonify({"_status_code":422,"error":"accountName not found"}),422)
    # else:
    return make_response(jsonify({"status_code":200, "followersCross": result}), 200)
    # else:
    #     return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)


@app.route('/addGeofenceOnBoard/',methods=['POST','OPTIONS','GET'])
def addGeofenceOnBoard():
    try:
        center = json.loads(request.data.decode('utf-8'))['center']
        radius = json.loads(request.data.decode('utf-8'))['radius']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    center = center.replace('(', '').replace(')', '').replace(' ', '').split(',')
    twits = getGeofenceTwits(center=center,radius=radius)
    if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
        return make_response(jsonify({"status_code":200,"twits":twits['twits']}),200)


@app.route('/addListCa/',methods=['POST','OPTIONS','GET'])
def addListCa():
    try:
        NewListCaName = json.loads(request.data.decode('utf-8'))['NewListCaName']
        CaNames = json.loads(request.data.decode('utf-8'))['CaNames']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    CaNames = CaNames.split(',')
    writeData({NewListCaName:CaNames},"./data/ca.json")
    return make_response(jsonify({"_status_code":200}),200)


# Analitica page
@app.route('/ListCa/',methods=['POST','OPTIONS','GET'])
def ListCa():
    try:
        start_time = time.time()
        ListCaName = json.loads(request.data.decode('utf-8'))['ListCaName'] 
        stat_twit_count = json.loads(request.data.decode('utf-8'))['stat_twit_count'] 
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    data = readData(name='./data/ca.json')[ListCaName]

    for ca_user in data:
        print('app.py ListCa() ca_user:', ca_user)
        twitter.get_last_tweets(api, ca_user, stat_twit_count)

    if len(data) != 0:
        answer = newGetTwitsEntity(data, stat_twit_count)
        print(f"--- {time.time() - start_time} seconds ---")
        return make_response(jsonify({"status_code": 200 ,"Ca": answer}), 200)
    else:
        return make_response(jsonify({"status_code": 404, "error": "There are not ca"}), 200)


@app.route('/getCountCaInList/',methods=['POST','OPTIONS','GET'])
def getCountCaInList():
    try:
        ListCaName = json.loads(request.data.decode('utf-8'))['ListCaName']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    data = readData(name='./data/ca.json')[ListCaName]
    CountCaInList = len(data)

    return make_response(jsonify({"status_code":200,"CountCaInList":CountCaInList}),200)


@app.route('/logs/',methods=['POST','OPTIONS','GET'])
def getLogs():
    path = os.path.join(os.getcwd(),"data","app.json")
    print(path)
    logs = readDataLogs(path)
    return make_response(jsonify({"logs":logs}),200)
    #return send_file(path,mimetype="application/json",as_attachment=False)


def readDataLogs(path):
    logs = {}
    with open(path, 'r',encoding='utf-8') as fh: #открываем файл с данными 
        line = fh.readlines()
    for log in reversed(line):
        data = json.loads(log)
        logs.update({f"{convertTime(data['time'])}":data})
    return(logs)


def convertTime(string):
    datetime_object = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f')
    return(datetime.strftime(datetime_object,"%H:%M %d-%m-%Y"))

def checkDatabase():
    if not os.path.exists("./app/data/tweets_ca.db"):
        print('run1')
        subprocess.run(['twint', "-u", "Boualemlabdoun1", '--database' ,"./app/data/tweets_ca.db"])
    if not os.path.exists("./app/data/database.db"):
        print('run2')
        subprocess.run(['twint', "-u", "Boualemlabdoun1", '--database' ,"./app/data/database.db"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

