import time
import flask
import logging
import os
import flask_login
from flask import render_template, request, jsonify, make_response, json,redirect
from numpy import e
import twitter
from twitter import getUserInfoDB,getFollowerInfoDB, getInfoAboutAccount, getInfoFromDB,chartHeatMapUpdate,getCountTwits,charttUpdate,getTwitsToBoard,get_followers,followersCross,followersCrossNames
import json_log_formatter
formatter = json_log_formatter.JSONFormatter()
from datetime import datetime
from flask_cors import CORS
from read_write import writeData, readData
import subprocess
import storage
import sqlite3
import tweepy


consumer_key = 'u4SD5KlVGm59ftBTb69glEtp1'
consumer_secret = 'PCSFhTShUoKzASdExZh5pz54nP1v4uo0KheBotPpZUUoQ3r1sV'
access_key = '2308267840-G9kog927ZlVhGvoUsXbIt16ZQLk0eUkeuteieA6'
access_secret = '6ZW7GNAZTG6tW4YXYShawMgGbv5ri4kfZvgDF1UAbSb4a'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


DATABASE = "./data/osiris.db"
storage.init(DATABASE)


app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'Shalom pravoslavny'
CORS(app)  # Change this!
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('./data/app.json')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

def set_logger(logger):
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = set_logger(logger)

class User(flask_login.UserMixin):
    pass

class AnonymousUser(flask_login.AnonymousUserMixin):
    pass

login_manager.anonymous_user = AnonymousUser
        
@login_manager.user_loader
def user_loader(login):
    user = User()
    user.id = login
    return user

@login_manager.request_loader
def request_loader(request):
    login = request.form.get('login')
    if (login != None)and(login not in users): 
        user = User()
        user.id = login
        return userhashtags
    elif (login != None):
        user = User()
        user.id = login
        return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("/login/")

@app.route('/logout/',methods=['GET','POST','OPTIONS'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
def logout():
    flask_login.logout_user()
    return redirect("/login/")

@app.route("/login/",methods=['GET','POST','OPTIONS'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    req = json.loads(request.data.decode('utf-8'))
    #req = 
    print(req)
    login = req['login']
    password = req['password']
    #users.update({login:{"password":"","files":[]}})
    #users = readData()
    users = ['useruser','banan']
    if (login in users) and (password == "test"):
        user = User()
        user.id = login
        flask_login.login_user(user)
        return make_response(jsonify('Oke'),200)
    else:
        return make_response(jsonify('Not good'),401)


@app.route("/",methods=['POST','OPTIONS','GET'])
@flask_login.login_required
def getDocuments():
    return render_template('index.html')

@app.route("/ca/",methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
@flask_login.login_required
def getCa():
    return render_template('ca.html')

@app.route("/analitica/",methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
@flask_login.login_required
def getAnalitica():
    try:
        data4 = readData(name='ca.json').keys()
        print(data4)
    except:
        data4 = "lol"
    return render_template('analitica.html',CaListNames=data4)

@app.route("/geofence/",methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
@flask_login.login_required
def getGeofence():
    return render_template('geofence.html')

@app.route("/infopovod/",methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
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
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    account = getInfoAboutAccount(api, twitterAccountName)
    
    if account['status_code'] != 200:
        logger.error({"error": "accountName is not found"})
        return make_response(jsonify({"_status_code":422,"error":"accountName is not found"}),422)
    else:
        twitterAccountName = account['user']['screen_name']
        user_info.update({"accountName": account['user']['name']})
        user_info.update({"screen_name": account['user']['screen_name']})
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
        else:
            print(weekdays) 

        weekdays_time = twitter.chartHeatMap2(twitterAccountName)
        if weekdays_time['status_code'] == 200:
            user_info.update({"weekdays_time": weekdays_time['weekdays_time']})
        else:
            print(weekdays_time) 
        
        langs = twitter.get_lang_count(twitterAccountName)
        if langs['status_code'] == 200:
            user_info.update({"langs": langs['langs'], "langCount": langs["langCount"]})
        else:
            print(langs)

        sources = twitter.get_source_count(twitterAccountName)
        if sources['status_code'] == 200:
            user_info.update({"sources": sources['sources'], "sourceCount": sources["sourceCount"]})
        else:
            print(sources)

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
        else:
            print(chartt)

        tweet_type = twitter.get_tweet_type_chart(twitterAccountName)
        if tweet_type['status_code'] == 200:
            user_info.update({"typeTweet": tweet_type['typeTweet'], "TypeCount": tweet_type["TypeCount"]})

        quotes_screen_name = twitter.get_tweet_quote_screen_name(twitterAccountName)
        print(quotes_screen_name)
        if quotes_screen_name['status_code'] == 200:
            user_info.update({"quote_screen_names": quotes_screen_name['quote_screen_names'], "quote_screen_name_count": quotes_screen_name["quote_screen_name_count"]})

        retweet_screen_names = twitter.get_tweet_retweet_screen_name(twitterAccountName)
        if quotes_screen_name['status_code'] == 200:
            user_info.update({"retweet_screen_names": retweet_screen_names['retweet_screen_names'], "retweet_screen_name_count": retweet_screen_names["retweet_screen_name_count"]})


        return make_response(jsonify(user_info), 200)

@app.route('/addDopMessage/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
def addDopMessage():
    try:
        twitterAccountName = json.loads(request.data.decode('utf-8'))['accountName']
        created_at = json.loads(request.data.decode('utf-8'))['created_at']
        print(f"+++++++++++++++++++++++++++{created_at}++++++++++++++++++++++++++++")
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    TwitsToBoard = getTwitsToBoard(twitterAccountName,created_at)
    if TwitsToBoard['status_code'] != 200:
        logger.error({"error": "TwitsToBoard not found"})
        return make_response(jsonify({"_status_code":404,"error":"TwitsToBoard not found"}),404)
    else:
        return make_response(jsonify({"TwitsToBoard":TwitsToBoard['TwitsToBoard'],"status_code":200}),200)

@app.route('/getTwits/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
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
    twits = getTwits([twitterAccountName],until=until,since=since)
    if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
        return make_response(jsonify({"status_code":200}),200)


@app.route('/addNewListInfluencers/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
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
        print(ListInfluencersName) # e.g. "Американские деятели"
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    data = readData()[ListInfluencersName]
    print(data)
    Influencers = []
    if len(data) != 0:
        for user in data:
            req = getUserInfoDB(user)
            if req['status_code'] == 200:
                Influencers.append(req['Influencer'])
    print(len(data))
    try:
        data2 = readData(name='followers_count.json')[ListInfluencersName]
        print(data2)
    except:
        data2 = False
    if False:# if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
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
        account = getInfoAboutAccount(accountName,bd=True)
        if account['status_code'] != 200:
            logger.error({"error": "accountName not found"})
            return make_response(jsonify({"_status_code":422,"error":"accountName not found"}),422)
        else:
            data.append(account['user']['username'])
            writeData({ListInfluencersName:data})

        return make_response(jsonify({"status_code":200,"Influencer":account['user']}),200)
    else:
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)

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
        # account = getInfoAboutAccount(accountName,bd=True)
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
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    data = readData()[ListInfluencersName]

    if len(data) != 0:
        result = get_followers(api, data, ListInfluencersName)
        if result['status_code'] != 200:
            logger.error({"error": "result not found"})
            return make_response(jsonify({"_status_code":422,"error":"accountName not found"}),422)
        else:
            return make_response(jsonify({"status_code":200}),200)
    else:
        return make_response(jsonify({"_status_code": 404, "error": "Twits not found"}), 404)
 
@app.route('/downloadFullFollowers/',methods=['POST','OPTIONS','GET'])
def downloadFullFollowers():
    try:
        print(request.data.decode('utf-8'))
        ListInfluencersName = json.loads(request.data.decode('utf-8'))['ListInfluencersName']
        cross_count = json.loads(request.data.decode('utf-8'))['crossCount']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    print(ListInfluencersName)
    data = readData()[ListInfluencersName]
    print(data)

    if len(data) != 0:
        ids = []
        for item in data:
            id = api.get_user(screen_name=item).id
            ids.append(id)

        result = followersCrossNames(ids, cross_count)
        if result['status_code'] != 200:
            logger.error({"error": "result not found"})
            return make_response(jsonify({"_status_code": 422, "error": "accountName not found"}),422)
        else:
            followersCrossNamess = result['followersCrossNames']
            if len(followersCrossNamess) != 0:
                users = []
                for username in followersCrossNamess:
                    ress = getFollowerInfoDB(username)
                    if ress['status_code'] == 200:
                        users.append(ress['Influencer'])
                        print("hello______________hello")
                    # else:
                        # users.append(getInfoAboutAccount(username,bd=True)['user'])
                print(users)
                return make_response(jsonify({"status_code":200,"ListInfluencersNames":users}),200)
            else:
                return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)

    else:
        return make_response(jsonify({"_status_code": 404, "error": "Twits not found"}), 404)

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
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
def addGeofenceOnBoard():
    try:
        center = json.loads(request.data.decode('utf-8'))['center']
        radius = json.loads(request.data.decode('utf-8'))['radius']
        # until = json.loads(request.data.decode('utf-8'))['until']
        # print(f"+++++++++++++++++++++++++++{until}++++++++++++++++++++++++++++")
        # since = json.loads(request.data.decode('utf-8'))['since']
        # print(f"+++++++++++++++++++++++++++{since}++++++++++++++++++++++++++++")
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    twits = getGeofenceTwits(center=center,radius=radius)
    if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
        return make_response(jsonify({"status_code":200,"twits":twits['twits']}),200) #twits['twits']
 
@app.route('/addListCa/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
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

@app.route('/ListCa/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
def ListCa():
    try:
        ListCaName = json.loads(request.data.decode('utf-8'))['ListCaName'] 
        stat_twit_count = json.loads(request.data.decode('utf-8'))['stat_twit_count'] 
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    data = readData(name='ca.json')[ListCaName]
    print(type(data))
    print(data)
    print(len(data))

    Ca = []
    if len(data) != 0:
        # for user in data:
            # req = getUserInfoDB(user)
            # if req['status_code'] == 200:
                # Ca.append(req['Influencer'])
        answer = newGetTwitsEntity(data,stat_twit_count)
    # print(len(Ca))
    if False:# if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
        return make_response(jsonify({"status_code":200,"Ca":answer}),200)

@app.route('/getCountCaInList/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
def getCountCaInList():
    try:
        ListCaName = json.loads(request.data.decode('utf-8'))['ListCaName']
    except:
        logger.error('"_status_code":422,"error": ["info":"incorrect POST-request"]')
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)
    data = readData(name='ca.json')[ListCaName]
    CountCaInList = len(data)
    # print(len(Ca))
    if False:# if twits['status_code'] != 200:
        logger.error({"error": "Twits not found"})
        return make_response(jsonify({"_status_code":404,"error":"Twits not found"}),404)
    else:
        return make_response(jsonify({"status_code":200,"CountCaInList":CountCaInList}),200)


@app.route('/logs/',methods=['POST','OPTIONS','GET'])
#@cross_origin(origins="*", methods=['POST','OPTIONS','GET'], allow_headers="*")
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

