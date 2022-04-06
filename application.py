import os, requests, hashlib, json
from random import getrandbits
from datetime import datetime, timedelta
from flask import Flask, session, render_template, request, make_response, abort, send_from_directory
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime as dt
from random import seed
from random import random
from random import randint
from haversine import haversine
import pandas as pd
import math

app = Flask(__name__, template_folder='./htmls')
app.secret_key = "secret"

DATABASE_URL = "postgresql://icnbjzbcznpgfp:a952b3bdc51644c4fb224f2dd8a7c358bc6a6e2fcf80a57a5e0d4956808d02a6@ec2-54-226-18-238.compute-1.amazonaws.com:5432/dbeqq9egku7fm5"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

port = int(os.environ.get('PORT', 5000))


def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/images/<path:filename>')
def base_static_images(filename):
    return send_from_directory(app.root_path + '/images/', filename)

@app.route('/vendor/<path:filename>')
def base_static_vendor(filename):
    return send_from_directory(app.root_path + '/vendor/', filename)

@app.route('/fonts/<path:filename>')
def base_static_fonts(filename):
    return send_from_directory(app.root_path + '/fonts/', filename)

@app.route('/scripts/<path:filename>')
def base_static_scripts(filename):
    return send_from_directory(app.root_path + '/scripts/', filename)

@app.route('/styles/<path:filename>')
def base_static_styles(filename):
    return send_from_directory(app.root_path + '/styles/', filename)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.execute("SELECT f_name, l_name, token, users.username FROM users, cell_tokens WHERE cell_tokens.username=users.username AND users.username = :username AND password = :password",
                    {"username": username, "password": password}).fetchone()

        # query_str = '?token='+user['token']+'&'+'username='+user['username']
        # print(query_str)
        if user != None and len(user) > 0:
            return render_template("main.html", token=user['token'], username=user['username'])
        else:
            return render_template("index.html", message="error")
    else:
        return render_template("index.html")


@app.route("/api/signin", methods=["GET"])#ok
def cell_signin_api():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        user = db.execute("SELECT f_name, l_name FROM users WHERE username = :username AND password = :password",
                    {"username": username, "password": password}).fetchone()
        if user != None and len(user) > 0:
            token = hashlib.md5(str(getrandbits(128)).encode('utf-8')).hexdigest()
            db.execute("INSERT INTO cell_tokens (username, token) VALUES (:username, :token)",
                {"username": username, "token": token})
            db.commit()
            res = '{"f_name":"' + user['f_name'] + '", "l_name":"' + user['l_name'] + '", "token":"' + token + '",' + '"message":"' + 'success' + '"}'
            res = json.loads(res)
            print(res)
            return res
        else:
            res = '{"message":"' + 'Incorrect login' + '"}'
            res = json.loads(res)
            print(res)
            return res
    except SQLAlchemyError as e:
        res = '{"message":"' + 'Error encountered ' + str(e.__dict__['orig']) + '"}'
        res = json.loads(res)
        print(res)
        return res

@app.route("/api/signout", methods=["GET"])
def cell_signout_api():
    try:
        username = request.args.get('username')
        token = request.args.get('token')
        user = db.execute("SELECT * FROM cell_tokens WHERE username = :username AND token = :token",
                    {"username": username, "token": token}).fetchone()
        if user != None and len(user) > 0:
            token = hashlib.md5(str(getrandbits(128)).encode('utf-8')).hexdigest()
            db.execute("DELETE FROM cell_tokens WHERE username = :username AND token = :token",
                {"username": username, "token": token})
            db.commit()
            res = '{"message":"' + 'success' + '"}'
            res = json.loads(res)
            print(res)
            return res
        else:
            res = '{"message":"' + 'Incorrect token' + '"}'
            res = json.loads(res)
            print(res)
            return res
    except SQLAlchemyError as e:
        res = '{"message":"' + 'Error encountered ' + str(e.__dict__['orig']) + '"}'
        res = json.loads(res)
        print(res)
        return res

@app.route("/api/signup", methods=["GET"])
def cell_signup_api():
    f_name = request.args.get('fname')
    l_name = request.args.get('lname')
    password = request.args.get('password')
    weight = request.args.get('weight')
    username = request.args.get('username')
    try:
        user = db.execute("SELECT * FROM users WHERE username = :username",
                    {"username": username}).fetchone()
        if user != None and len(user) > 0:
            res = '{"message":"' + 'User already exists' + '"}'
            res = json.loads(res)
            return res
        else:
            db.execute("INSERT INTO users (f_name, l_name, username, password, weight) VALUES (:firstname, :lastname, :username, :password, :weight)",
                {"firstname": f_name, "lastname": l_name, "username": username, "password": password, "weight": weight})
            db.commit()
            res = '{"message":"' + 'success' + '"}'
            res = json.loads(res)
            return res
    except SQLAlchemyError as e:
        res = '{"message":"' + 'Error encountered ' + str(e.__dict__['orig']) + '"}'
        res = json.loads(res)
        return res

@app.route("/api/destinations_feedbacks", methods=["GET"])
def destinations_feedbacks():
    # token + '|' + type + '|' + name + '|' + lat + '|' + '|' + lng
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    type = request.args.get('type')
    username = request.args.get('username')
    name = request.args.get('name')
    username = cell_auth(token)
    avg_rate = 0
    votes = 0
    if username == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    comments = db.execute("SELECT * FROM dst_feedbacks WHERE type = :type AND lat = :lat AND lng = :lng AND name = :name",
                {"type": type, "lat": lat, "lng": lng, "name": name}).fetchall()
    agg_feed = db.execute("SELECT avg(rate) AS rates, count(*) AS votes FROM dst_feedbacks WHERE type = :type AND lat = :lat AND lng = :lng AND name = :name",
                {"type": type, "lat": lat, "lng": lng, "name": name}).fetchone()
    feedbacks = []
    for comment in comments:
        feedbacks += [{"rate": comment['rate'],"feedback": comment['comment']}]
    # feedbacks = json.dumps([{"rate":"2.5","feedback": "Descent place."}])
    feedbacks = json.dumps(feedbacks)
    if (agg_feed['rates'] == None or agg_feed['rates'] == "null"):
        avg_rate = 0
    else:
        avg_rate = agg_feed['rates']
    votes = agg_feed['votes']
    res = '{"message":"' + 'success' + '", "rate":' + str(avg_rate) + ', "votes":' + str(votes) + ', "feedbacks":' + feedbacks + '}'
    res = json.loads(res)
    return res

def cell_auth(token):
    user = db.execute("SELECT * FROM cell_tokens WHERE token = :token",
                {"token": token}).fetchone()
    try:
        return user['username']
    except:
        return False

@app.route("/api/gototoilet", methods=["GET"])
def gototoilet():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius')
    coordinates = []
    res = json.dumps({"message":"error"})
    res = json.loads(res)
    if cell_auth(token) == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        responses = requests.get('https://data.calgary.ca/resource/jjkg-kv4n.json?asset_type=WASHROOM&$where=within_circle(the_geom,'+lat+','+lng+','+radius+')').json()
        if len(responses) > 0:
            rnd = random()
            rand = randint(0, len(responses)-1)
            print(len(responses)-1)
            print(rand)
            if (rnd > 0.5):
                for response in responses:
                    dst_lat = response['latitude']
                    dst_lng = response['longitude']
                    coordinates += [(dst_lat,dst_lng)]
                query_str = "select lat,lng,avg(rate) as rates from toilets_feedbacks group by lat,lng order by rates desc"
                points = db.execute(query_str).fetchall()
                for point in points:
                    if (point[0],point[1]) in coordinates:
                        res = json.dumps({"message":"success", "lat":point[0], "lng":point[1]})
                        res = json.loads(res)
                        return res
                res = json.dumps({"message":"success", "lat":responses[rand]['latitude'], "lng":responses[rand]['longitude']})
                res = json.loads(res)
                return res
            else:
                res = json.dumps({"message":"success", "lat":responses[rand]['latitude'], "lng":responses[rand]['longitude']})
                res = json.loads(res)
                return res
        else:
            res = json.dumps({"message":"error"})
    except SQLAlchemyError as e:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
    res = json.dumps({"message":"error"})
    res = json.loads(res)
    return res

@app.route("/api/gotowater", methods=["GET"])
def gotowater():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius')
    coordinates = []
    res = json.dumps({"message":"error"})
    res = json.loads(res)
    if cell_auth(token) == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        responses = requests.get('https://data.calgary.ca/resource/jjkg-kv4n.json?asset_type=DRINKING FOUNTAIN&$where=within_circle(the_geom,'+lat+','+lng+','+radius+')').json()
        if len(responses) > 0:
            rnd = random()
            rand = randint(0, len(responses)-1)
            print(len(responses)-1)
            print(rand)
            if (rnd > 0.5):
                for response in responses:
                    dst_lat = response['latitude']
                    dst_lng = response['longitude']
                    coordinates += [(dst_lat,dst_lng)]
                query_str = "select lat,lng,avg(rate) as rates from water_feedbacks group by lat,lng order by rates desc"
                points = db.execute(query_str).fetchall()
                for point in points:
                    if (point[0],point[1]) in coordinates:
                        res = json.dumps({"message":"success", "lat":point[0], "lng":point[1]})
                        res = json.loads(res)
                        return res
                res = json.dumps({"message":"success", "lat":responses[rand]['latitude'], "lng":responses[rand]['longitude']})
                res = json.loads(res)
                return res
            else:
                res = json.dumps({"message":"success", "lat":responses[rand]['latitude'], "lng":responses[rand]['longitude']})
                res = json.loads(res)
                return res
        else:
            res = json.dumps({"message":"error"})
    except SQLAlchemyError as e:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
    res = json.dumps({"message":"error"})
    res = json.loads(res)
    return res

@app.route("/api/gotobench", methods=["GET"])
def gotobench():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius')
    coordinates = []
    res = json.dumps({"message":"error"})
    res = json.loads(res)
    if cell_auth(token) == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        print("wrong token")
        return res
    try:
        responses = requests.get('https://data.calgary.ca/resource/ikeb-n5bc.json?$where=within_circle(location,'+lat+','+lng+','+radius+')').json()
        if len(responses) > 0:
            rnd = random()
            rand = randint(0, len(responses)-1)
            print(len(responses)-1)
            print(rand)
            if (rnd > 0.5):
                print("enter exploit")
                for response in responses:
                    dst_lat = response['latitude']
                    dst_lng = response['longitude']
                    coordinates += [(dst_lat,dst_lng)]
                query_str = "select lat,lng,avg(rate) as rates from benches_feedbacks group by lat,lng order by rates desc"
                points = db.execute(query_str).fetchall()
                for point in points:
                    if (point[0],point[1]) in coordinates:
                        print("with comment" + point[0] + " " + point[1])
                        res = json.dumps({"message":"success", "lat":point[0], "lng":point[1]})
                        res = json.loads(res)
                        return res
                print("no comment " + responses[rand]['latitude'] + " " + responses[rand]['longitude'])
                res = json.dumps({"message":"success", "lat":responses[rand]['latitude'], "lng":responses[rand]['longitude']})
                print(res)
                res = json.loads(res)
                return res
            else:
                print("enter explore " + responses[rand]['latitude'] + " " + responses[rand]['longitude'])
                res = json.dumps({"message":"success", "lat":responses[rand]['latitude'], "lng":responses[rand]['longitude']})
                print(res)
                res = json.loads(res)
                return res
        else:
            res = json.dumps({"message":"error"})
    except SQLAlchemyError as e:
        print("except")
        res = json.dumps({"message":"error"})
        res = json.loads(res)
    res = json.dumps({"message":"error"})
    res = json.loads(res)
    return res

@app.route("/api/benchfeedback", methods=["GET"])
def benchfeedback():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    rate = request.args.get('rate')
    username = cell_auth(token)
    if username == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        db.execute("INSERT INTO benches_feedbacks (username, lat, lng, rate) VALUES (:username, :lat, :lng, :rate)",
            {"username": username, "lat": lat, "lng": lng, "rate": rate})
        db.commit()
        res = json.dumps({"message":"success"})
    except SQLAlchemyError as e:
        res = json.dumps({"message":"error"})
    res = json.loads(res)
    return res

@app.route("/api/toiletfeedback", methods=["GET"])
def toiletfeedback():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    rate = request.args.get('rate')
    username = cell_auth(token)
    if username == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        db.execute("INSERT INTO toilets_feedbacks (username, lat, lng, rate) VALUES (:username, :lat, :lng, :rate)",
            {"username": username, "lat": lat, "lng": lng, "rate": rate})
        db.commit()
        res = json.dumps({"message":"success"})
    except SQLAlchemyError as e:
        res = json.dumps({"message":"error"})
    res = json.loads(res)
    return res

@app.route("/api/waterfeedback", methods=["GET"])
def waterfeedback():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    rate = request.args.get('rate')
    username = cell_auth(token)
    if username == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        db.execute("INSERT INTO water_feedbacks (username, lat, lng, rate) VALUES (:username, :lat, :lng, :rate)",
            {"username": username, "lat": lat, "lng": lng, "rate": rate})
        db.commit()
        res = json.dumps({"message":"success"})
    except SQLAlchemyError as e:
        res = json.dumps({"message":"error"})
    res = json.loads(res)
    return res

@app.route("/api/changepassword", methods=["GET"])
def changepassword():
    token = request.args.get('token')
    new_password = request.args.get('password')
    username = cell_auth(token)
    if username == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        db.execute("UPDATE users SET password = :password WHERE username = :username",
            {"username": username, "password": new_password})
        db.commit()
        res = '{"message":"' + 'success' + '"}'
        res = json.loads(res)
        return res
    except:
        res = '{"message":"' + 'error' + '"}'
        res = json.loads(res)
        return res

@app.route("/api/changeweight", methods=["GET"])
def changeweight():
    token = request.args.get('token')
    new_weight = request.args.get('weight')
    username = cell_auth(token)
    if username == False:
        res = json.dumps({"message":"error"})
        res = json.loads(res)
        return res
    try:
        db.execute("UPDATE users SET weight = :weight WHERE username = :username",
            {"username": username, "weight": new_weight})
        db.commit()
        res = '{"message":"' + 'success' + '"}'
        res = json.loads(res)
        return res
    except:
        res = '{"message":"' + 'error' + '"}'
        res = json.loads(res)
        return res

@app.route("/api/feedback", methods=["POST"])
def feedback():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    name = request.args.get('name')
    type = request.args.get('type')
    content = request.json
    rate = content['rate']
    comment = content['comment']
    username = cell_auth(token)
    if username == False:
        res = json.dumps({"message":"incorrect token"})
        res = json.loads(res)
        return res
    try:
        db.execute("INSERT INTO dst_feedbacks (username, type, name, lat, lng, rate, comment) VALUES (:username, :type, :name, :lat, :lng, :rate, :comment)",
            {"username": username, "type": type, "name": name, "lat": lat, "lng": lng, "rate": rate, "comment": comment})
        db.commit()
        res = '{"message":"' + 'success' + '"}'
        res = json.loads(res)
        return res
    except SQLAlchemyError as e:
        res = '{"message":"' + 'error' + '"}'
        res = json.loads(res)
        return res

@app.route("/api/location_update", methods=["GET"])
def location_update():
    token = request.args.get('token')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    username = cell_auth(token)
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    # print(timestamp)
    if username == False:
        res = json.dumps({"message" : "incorrect token"})
        res = json.loads(res)
        return res
    try:
        db.execute("INSERT INTO trajectories (username, lat, lng, timestamp) VALUES (:username, :lat, :lng, to_timestamp(:timestamp, 'dd-mm-yyyy hh24:mi:ss'))",
            {"username": username, "lat": lat, "lng": lng, "timestamp": timestamp})
        db.commit()
        res = '{"message":"' + 'success' + '"}'
        res = json.loads(res)
        return res
    except SQLAlchemyError as e:
        res = '{"message":"' + 'error' + '"}'
        res = json.loads(res)
        return res

@app.route("/api/get_stats", methods=["GET"])
def get_stats():
    token = request.args.get('token')
    username = cell_auth(token)
    # print(timestamp)
    timestamp_today = datetime.now().strftime("%Y-%m-%d")
    timestamp_lastweek = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    # if str(timestamp_lastweek) < (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"):
    #     print("yes")
    this_week = [0, 0, 0, 0, 0, 0, 0]
    this_month = 0
    this_week_overall_time = [0, 0, 0, 0, 0, 0, 0]
    this_month_overall_time = 0
    if username == False:
        res = json.dumps({"message" : "incorrect token"})
        res = json.loads(res)
        return res
    try:
        weight = db.execute("SELECT weight FROM public.users WHERE username = :username",
            {"username": username}).fetchone()['weight']
        entries = db.execute("SELECT date_trunc('day', timestamp)::date date, timestamp, lat, lng FROM public.trajectories WHERE date_trunc('day', timestamp) > CURRENT_DATE - 30 AND username = :username order by date desc",
            {"username": username})
        df = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
        prev = df.iloc[0]
        for index, entry in df[1:].iterrows():
            x = (prev['lat'], prev['lng'])
            y = (entry['lat'], entry['lng'])
            # td = abs((datetime.strptime(str(prev['timestamp']), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(entry['timestamp']), "%Y-%m-%d %H:%M:%S")).minute)
            a=datetime.strptime(str(prev['timestamp']), "%Y-%m-%d %H:%M:%S")
            b=a-datetime.strptime(str(entry['timestamp']), "%Y-%m-%d %H:%M:%S")
            td=abs(b.total_seconds())
            a=datetime.strptime(str(entry['date']), "%Y-%m-%d")
            b=datetime.strptime(str(timestamp_today), "%Y-%m-%d")-a
            dd=abs(b.days)
            if(dd < 7 and str(prev['date']) == str(entry['date']) and abs(td) < 10800):
                this_week[dd] += abs(haversine((prev['lat'], prev['lng']), (entry['lat'], entry['lng'])) * 1000)
                this_week_overall_time[dd] += abs(td)
            if(str(prev['date']) == str(entry['date']) and abs(td) < 10800):
                this_month += abs(haversine(x, y) * 1000)
                this_month_overall_time += abs(td)
            prev = entry
        this_week_cals = [7.2 * weight * entry / 3600 for entry in this_week_overall_time]
        this_month_cals = 7.2 * weight * this_month_overall_time / 3600
        # print(this_week_cals)
        # print(this_month_cals)
        res = json.dumps({"message":"success", "weekly":this_week_cals, "monthly":this_month_cals})
        # print(res)
        res = json.loads(res)
        return res
    except Exception as e:
        res = json.loads('{"message":"' + 'error' + '"}')
        return res
    res = json.loads('{"message":"' + 'error' + '"}')
    return res


@app.route("/api/get_range_stats", methods=["GET"])
def get_range_stats():
    token = request.args.get('token')
    start = request.args.get('start')
    end = request.args.get('end')
    username = cell_auth(token)
    startDate = datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.strptime(end, "%Y-%m-%d")
    days = (endDate - startDate).days + 1
    dateArray = [0] * days
    overall_time = [0] * days
    overall_dist = [0] * days
    # dateArray = [randint(0,4000)] * days
    weight = db.execute("SELECT weight FROM public.users WHERE username = :username",
        {"username": username}).fetchone()['weight']
    entries = db.execute("SELECT date_trunc('day', timestamp)::date date, timestamp, lat, lng FROM public.trajectories WHERE date_trunc('day', timestamp) >= :startDate AND date_trunc('day', timestamp) <= :endDate AND username = :username order by date desc",
        {"username": username, "startDate":startDate, "endDate":endDate})
    df = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
    try:
        prev = df.iloc[0]
        for index, entry in df[1:].iterrows():
            x = (prev['lat'], prev['lng'])
            y = (entry['lat'], entry['lng'])
            a=datetime.strptime(str(prev['timestamp']), "%Y-%m-%d %H:%M:%S")
            b=a-datetime.strptime(str(entry['timestamp']), "%Y-%m-%d %H:%M:%S")
            td=abs(b.total_seconds())
            a=datetime.strptime(str(entry['date']), "%Y-%m-%d")
            b=startDate-a
            dd=abs(b.days)
            if(str(prev['date']) == str(entry['date']) and abs(td) < 10800):
                overall_dist[dd] += abs(haversine(x, y) * 1000)
                overall_time[dd] += abs(td)
            dateArray = [7.2 * weight * entry / 3600 for entry in overall_time]
            prev = entry
    except:
        pass
    res = json.dumps({"message":"success","days":len(dateArray), "data":dateArray, "average":sum(dateArray)/len(dateArray), "total":sum(dateArray)})
    print(res)
    res = json.loads(res)
    return res
