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
import pyrebase
from urllib.request import urlopen
from pykalman import KalmanFilter
# from firebase import firebase

app = Flask(__name__, template_folder='./htmls')
app.secret_key = "secret"
secret_key = "324324"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

kf = KalmanFilter();

config = {

}

firbase = pyrebase.initialize_app(config)
database = firbase.database()


# firebase = firebase.FirebaseApplication("https://engo-651-final-project-default-rtdb.firebaseio.com/", None)









DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/images/<path:filename>')
def base_static_images(filename):
    return send_from_directory(app.root_path + '/images/', filename)

@app.route('/assets/<path:filename>')
def base_static_assets(filename):
    return send_from_directory(app.root_path + '/assets/', filename)

@app.route('/includes/<path:filename>')
def base_static_includes(filename):
    return send_from_directory(app.root_path + '/htmls/includes/', filename)

@app.route('/layouts/<path:filename>')
def base_static_layouts(filename):
    return send_from_directory(app.root_path + '/htmls/layouts/', filename)

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


# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = db.execute("SELECT f_name, l_name, token, users.username FROM users, cell_tokens WHERE cell_tokens.username=users.username AND users.username = :username AND password = :password",
#                     {"username": username, "password": password}).fetchone()
#
#         # query_str = '?token='+user['token']+'&'+'username='+user['username']
#         # print(query_str)
#         if user != None and len(user) > 0:
#             return render_template("main.html", token=user['token'], username=user['username'])
#         else:
#             return render_template("index.html", message="error")
#     else:
#         return render_template("index.html")


# @app.route("/api/signin", methods=["GET"])#ok
# def cell_signin_api():
#     try:
#         username = request.args.get('username')
#         password = request.args.get('password')
#         user = db.execute("SELECT f_name, l_name FROM users WHERE username = :username AND password = :password",
#                     {"username": username, "password": password}).fetchone()
#         if user != None and len(user) > 0:
#             token = hashlib.md5(str(getrandbits(128)).encode('utf-8')).hexdigest()
#             db.execute("INSERT INTO cell_tokens (username, token) VALUES (:username, :token)",
#                 {"username": username, "token": token})
#             db.commit()
#             res = '{"f_name":"' + user['f_name'] + '", "l_name":"' + user['l_name'] + '", "token":"' + token + '",' + '"message":"' + 'success' + '"}'
#             res = json.loads(res)
#             print(res)
#             return res
#         else:
#             res = '{"message":"' + 'Incorrect login' + '"}'
#             res = json.loads(res)
#             print(res)
#             return res
#     except SQLAlchemyError as e:
#         res = '{"message":"' + 'Error encountered ' + str(e.__dict__['orig']) + '"}'
#         res = json.loads(res)
#         print(res)
#         return res

@app.route("/profile", methods=["GET", "POST"])
def profile():
    pass_changed = False
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')
    fullname = request.cookies.get('fullname')
    message = ""
    if request.method == "POST":
        new_email = request.form["input-email"]
        new_weight = request.form["input-weight"]
        new_pass = request.form["input-pass"]
        new_repass = request.form["input-repass"]
        info = request.form["info"]
        database.child("users").child(username).child('weight').set(new_weight)
        database.child("users").child(username).child('email').set(new_email)
        database.child("users").child(username).child('info').set(info)
        message = "update"
        if (new_pass == new_repass and new_repass != ""):
            new_pass = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
            database.child("users").child(username).child('password').set(new_pass)
            pass_changed = True
            session_id = str(username) + str(secret_key) + str(new_pass)
            session_id = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
        elif (new_repass != new_pass):
            message = "not_same"
    query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
    passw = json.load(urlopen(query_string))
    query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/weight.json"
    weight = json.load(urlopen(query_string))
    query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/firstname.json"
    firstname = json.load(urlopen(query_string))
    query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/lastname.json"
    lastname = json.load(urlopen(query_string))
    query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/email.json"
    email = json.load(urlopen(query_string))
    try:
        # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/info.json"
        # info = json.load(urlopen(query_string))
        info = database.child("users").child(username).child('info').get().val()
        # print(info)
    except:
        info = ""
    # print(email )
    logged_devs = 0
    try:
        query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens.json?orderBy=%22username%22&equalTo=%22" + username + "%22"
        reqs = json.load(urlopen(query_string))
        logged_devs = len(reqs.keys())
    except:
        pass
    comments=0
    try:
        req = db.execute("select * from dst_feedbacks where username=:username",
                    {"username": username}).fetchall()
        comments = len(req)
    except:
        pass
    feedbacks=0
    try:
        req = db.execute("select * from benches_feedbacks where username=:username",
                    {"username": username}).fetchall()
        feedbacks = len(req)
        req = db.execute("select * from toilets_feedbacks where username=:username",
                    {"username": username}).fetchall()
        feedbacks += len(req)
        req = db.execute("select * from water_feedbacks where username=:username",
                    {"username": username}).fetchall()
        feedbacks += len(req)
    except:
        pass
    if web_auth(session_id, username, passw):
        if (info == None or info == ""):
            ret = make_response(render_template("profile.html", message=message, feedbacks=feedbacks, comments=comments, logged_devs=logged_devs, password=passw, email=email, lastname=lastname, firstname=firstname, username=username, fullname=fullname, weight=weight))
            if pass_changed:
                ret.set_cookie('session_id', session_id)
            return ret
        else:
            ret = make_response(render_template("profile.html", message=message, info=info, feedbacks=feedbacks, comments=comments, logged_devs=logged_devs, password=passw, email=email, lastname=lastname, firstname=firstname, username=username, fullname=fullname, weight=weight))
            if pass_changed:
                ret.set_cookie('session_id', session_id)
            return ret
    else:
        return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')
    fullname = request.cookies.get('fullname')
    # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
    # passw = json.load(urlopen(query_string))
    passw = database.child("users").child(username).child('password').get().val()
    if web_auth(session_id, username, passw):
        return render_template("home.html", username=username, fullname=fullname)
    else:
        return render_template("index.html")

@app.route("/track", methods=["GET", "POST"])
def track():
    if request.method == "POST":
        username = request.cookies.get('username')
        session_id = request.cookies.get('session_id')
        query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
        passw = json.load(urlopen(query_string))
        bike = int(request.args.get('bike'))
        query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens.json?orderBy=%22username%22&equalTo=%22" + username + "%22"
        reqs = json.load(urlopen(query_string))
        tokens = [*reqs]
        token = tokens[bike]
        print(token)
        if web_auth(session_id, username, passw):
            return render_template("main.html", username=username, token=token)
        else:
            return render_template("index.html")
    else:
        session_id = request.cookies.get('session_id')
        username = request.cookies.get('username')
        fullname = request.cookies.get('fullname')
        # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
        # passw = json.load(urlopen(query_string))
        passw = database.child("users").child(username).child('password').get().val()
        query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens.json?orderBy=%22username%22&equalTo=%22" + username + "%22"
        reqs = json.load(urlopen(query_string))
        num_dev = len(reqs.keys())
        print("num_dev: "+str(num_dev))
        if web_auth(session_id, username, passw):
            return render_template("track.html", num_dev=num_dev, username=username, fullname=fullname)
        else:
            return render_template("index.html")

def track_bike(bike):
    print("track bike"+str(bike))

@app.route("/destination", methods=["GET", "POST"])
def destination():
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')
    fullname = request.cookies.get('fullname')
    # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
    # passw = json.load(urlopen(query_string))
    passw = database.child("users").child(username).child('password').get().val()
    if web_auth(session_id, username, passw):
        return render_template("destination.html", username=username, fullname=fullname)
    else:
        return render_template("index.html")

@app.route("/map", methods=["GET", "POST"])
def map():
    return render_template("map.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    session_id = request.cookies.get('session_id')
    username = request.cookies.get('username')
    fullname = request.cookies.get('fullname')
    total_time_today = 0
    total_time_today_up = 0
    total_dist_today = 0
    total_dist_today_up = 0
    total_time_week = 0
    total_time_week_up = 0
    total_dist_week = 0
    total_dist_week_up = 0
    time_today = datetime.now().strftime("%Y-%m-%d")
    time_lasttwoweek = (datetime.now() - timedelta(days=13)).strftime("%Y-%m-%d")
    days, overall_time, overall_dist, overall_cals = cal_prams(time_lasttwoweek, time_today, username)
    total_time_today = overall_time[days-1]
    total_time_today_up  = (overall_time[days-1] - overall_time[days-2])
    total_dist_today = overall_dist[days-1]/1000
    total_dist_today_up  = ((overall_dist[days-1] - overall_dist[days-2])/1000)
    # print(days, overall_time, overall_dist, overall_cals)
    # print(overall_time[0: 7])
    total_time_week = sum(overall_time[days-8: days-1])/60
    total_time_week_up = (total_time_week - sum(overall_time[0: 7])/60)
    total_dist_week = sum(overall_dist[days-8: days-1])/1000
    total_dist_week_up = (total_dist_week - sum(overall_dist[0: 7])/1000)
    # print(str(overall_cals[6:]))
    # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
    # passw = json.load(urlopen(query_string))
    passw = database.child("users").child(username).child('password').get().val()
    if web_auth(session_id, username, passw):
        return render_template("dashboard.html", total_time_today=int(total_time_today),
        total_time_today_up=int(total_time_today_up), total_dist_today=int(total_dist_today),
        total_dist_today_up=int(total_dist_today_up), total_time_week=int(total_time_week),
        total_time_week_up=int(total_time_week_up), total_dist_week=int(total_dist_week),
        total_dist_week_up=int(total_dist_week_up), kcals_week0=int(overall_dist[7]),
        kcals_week1=int(overall_dist[8]), kcals_week2=int(overall_dist[9]), kcals_week3=int(overall_dist[10]),
        kcals_week4=int(overall_dist[11]), kcals_week5=int(overall_dist[12]), kcals_week6=int(overall_dist[13]),
        username=username, fullname=fullname, kcals_week_day0=(datetime.now() - timedelta(days=6)).strftime("%m-%d"),
        kcals_week_day1=(datetime.now() - timedelta(days=5)).strftime("%m-%d"),
        kcals_week_day2=(datetime.now() - timedelta(days=4)).strftime("%m-%d"),
        kcals_week_day3=(datetime.now() - timedelta(days=3)).strftime("%m-%d"),
        kcals_week_day4=(datetime.now() - timedelta(days=2)).strftime("%m-%d"),
        kcals_week_day5=(datetime.now() - timedelta(days=1)).strftime("%m-%d"),
        kcals_week_day6=(datetime.now().strftime("%m-%d")),
        kcals_day0=(datetime.now() - timedelta(days=9)).strftime("%m-%d"),
        kcals_day1=(datetime.now() - timedelta(days=8)).strftime("%m-%d"),
        kcals_day2=(datetime.now() - timedelta(days=7)).strftime("%m-%d"),
        kcals_day3=(datetime.now() - timedelta(days=6)).strftime("%m-%d"),
        kcals_day4=(datetime.now() - timedelta(days=5)).strftime("%m-%d"),
        kcals_day5=(datetime.now() - timedelta(days=4)).strftime("%m-%d"),
        kcals_day6=(datetime.now() - timedelta(days=3)).strftime("%m-%d"),
        kcals_day7=(datetime.now() - timedelta(days=2)).strftime("%m-%d"),
        kcals_day8=(datetime.now() - timedelta(days=1)).strftime("%m-%d"),
        kcals_day9=(datetime.now().strftime("%m-%d")), kcals_0=int(overall_cals[4]),
        kcals_1=int(overall_cals[5]), kcals_2=int(overall_cals[6]), kcals3=int(overall_cals[7]),
        kcals_4=int(overall_cals[8]), kcals_5=int(overall_cals[9]), kcals6=int(overall_cals[10]),
        kcals_7=int(overall_cals[11]), kcals_8=int(overall_cals[12]), kcals_9=int(overall_cals[13]))
    else:
        return render_template("index.html")

def cal_prams(start, end, username):
    startDate = datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.strptime(end, "%Y-%m-%d")
    days = (endDate - startDate).days + 1
    dateArray = [0] * days
    overall_time = [0] * days
    overall_dist = [0] * days
    # dateArray = [randint(0,4000)] * days
    # weight = db.execute("SELECT weight FROM public.users WHERE username = :username",
    #     {"username": username}).fetchone()['weight']
    # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/weight.json"
    # weight = int(json.load(urlopen(query_string)))
    weight = int(database.child("users").child(username).child("weight").get().val())
    # print(weight)
    entries = db.execute("SELECT date_trunc('day', timestamp)::date date, timestamp, lat, lng FROM public.trajectories WHERE date_trunc('day', timestamp) >= :startDate AND date_trunc('day', timestamp) <= :endDate AND username = :username order by date desc",
        {"username": username, "startDate":startDate, "endDate":endDate})
    df = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
    # print(df)
    # df_old = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
    df_new = df[['date', 'timestamp']]
    array = df.to_numpy()[:,2:]
    array = douglas_kalman_smoothing(array)
    print(array.shape)
    df_new['lat'] = array[:,0].tolist()
    df_new['lng'] = array[:,1].tolist()
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
        # print(e)
    return days, overall_time, overall_dist, dateArray

@app.route("/logout", methods=["GET", "POST"])
def logout():
    ret = make_response(render_template("index.html"))
    ret.set_cookie('session_id', "")
    ret.set_cookie('username', "")
    ret.set_cookie('fullname', "")
    return ret

@app.route("/", methods=["GET", "POST"])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
            # passw = json.load(urlopen(query_string))
            passw = database.child("users").child(username).child('password').get().val()
            # print(password)
            # print(passw)
            if passw != None and len(passw) > 0 and passw == password:
                # db.execute("INSERT INTO cell_tokens (username, token) VALUES (:username, :token)",
                    # {"username": username, "token": token})
                # db.commit()
                # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens.json?orderBy=%22username%22&equalTo=%22" + username + "%22"
                # reqs = json.load(urlopen(query_string))
                # keys = [k for k in reqs.keys()]
                # token = keys
                query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/" + username + "/firstname.json"
                reqs = json.load(urlopen(query_string))
                f_name = reqs
                query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/" + username + "/lastname.json"
                reqs = json.load(urlopen(query_string))
                l_name = reqs
                fullname = f_name + " " + l_name
                # ret = render_template("dashboard.html", token=token, username=username, fullname=fullname)
                ret = make_response(render_template("home.html", username=username, fullname=fullname))
                session_id = str(username) + str(secret_key) + str(password)
                session_id = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
                ret.set_cookie('session_id', session_id)
                ret.set_cookie('username', username)
                ret.set_cookie('fullname', fullname)
                return ret
            else:
                return render_template("index.html", message="error")
        else:
            try:
                session_id = request.cookies.get('session_id')
                username = request.cookies.get('username')
                fullname = request.cookies.get('fullname')
                # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
                # passw = json.load(urlopen(query_string))
                passw = database.child("users").child(username).child('password').get().val()
                if web_auth(session_id, username, passw):
                    return render_template("home.html", username=username, fullname=fullname)
                else:
                    return render_template("index.html")
            except:
                # print(e.message)
                return render_template("index.html")
    except Exception as e:
        print(e.message)
        return render_template("index.html", message="error")

def web_auth(session_id, username, password):
    c_session_id = str(username) + str(secret_key) + str(password)
    c_session_id = hashlib.sha256(c_session_id.encode('utf-8')).hexdigest()
    return c_session_id == session_id

@app.route("/api/signin", methods=["GET"])#ok
def cell_signin_api():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # user = db.execute("SELECT f_name, l_name FROM users WHERE username = :username AND password = :password",
                    # {"username": username, "password": password}).fetchone()
        # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/password.json"
        # passw = json.load(urlopen(query_string))
        passw = database.child("users").child(username).child('password').get().val()
        # pass = user[0].password
        # print (passw)
        if passw != None and len(passw) > 0 and passw == password:
            token = hashlib.md5(str(getrandbits(128)).encode('utf-8')).hexdigest()
            # db.execute("INSERT INTO cell_tokens (username, token) VALUES (:username, :token)",
                # {"username": username, "token": token})
            # db.commit()
            data =  {"username": username, "token": token}
            # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/firstname.json"
            # f_name = json.load(urlopen(query_string))
            f_name = database.child("users").child(username).child('firstname').get().val()
            # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/lastname.json"
            # passw = json.load(urlopen(query_string))
            l_name = database.child("users").child(username).child('lastname').get().val()
            res = '{"f_name":"' + f_name + '", "l_name":"' + l_name + '", "token":"' + token + '",' + '"message":"' + 'success' + '"}'
            # res = '{"message":"' + 'login' + '"}'
            database.child("tokens").child(token).set(data)
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
        query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens.json?orderBy=%22username%22&equalTo=%22" + username + "%22"
        reqs = json.load(urlopen(query_string))
        if reqs != None and len(reqs.keys()) > 0:
            # db.execute("DELETE FROM cell_tokens WHERE username = :username AND token = :token",
            #     {"username": username, "token": token})
            # db.commit()
            database.child("tokens").child(token).remove()
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

# @app.route("/api/signup", methods=["GET"])
# def cell_signup_api():
#     f_name = request.args.get('fname')
#     l_name = request.args.get('lname')
#     password = request.args.get('password')
#     weight = request.args.get('weight')
#     username = request.args.get('username')
#     try:
#         user = db.execute("SELECT * FROM users WHERE username = :username",
#                     {"username": username}).fetchone()
#         if user != None and len(user) > 0:
#             res = '{"message":"' + 'User already exists' + '"}'
#             res = json.loads(res)
#             return res
#         else:
#             db.execute("INSERT INTO users (f_name, l_name, username, password, weight) VALUES (:firstname, :lastname, :username, :password, :weight)",
#                 {"firstname": f_name, "lastname": l_name, "username": username, "password": password, "weight": weight})
#             db.commit()
#             res = '{"message":"' + 'success' + '"}'
#             res = json.loads(res)
#             return res
#     except SQLAlchemyError as e:
#         res = '{"message":"' + 'Error encountered ' + str(e.__dict__['orig']) + '"}'
#         res = json.loads(res)
#         return res

@app.route("/api/signup", methods=["GET"])
def cell_signup_api():
    f_name = request.args.get('fname')
    l_name = request.args.get('lname')
    password = request.args.get('password')
    weight = request.args.get('weight')
    email = request.args.get('email')
    username = request.args.get('username')
    try:
        user = database.child("users").order_by_child("username").equal_to(username).get()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/username.json"
        # user = json.load(urlopen(query_string))
        # if user != None and len(user) > 0:
        # print(user)
        if user != None:
            res = '{"message":"' + 'User already exists' + '"}'
            res = json.loads(res)
            return res
        else:
            # db.execute("INSERT INTO users (f_name, l_name, username, password, weight) VALUES (:firstname, :lastname, :username, :password, :weight)",
            #     {"firstname": f_name, "lastname": l_name, "username": username, "password": password, "weight": weight})
            # db.commit()
            data = {
                "firstname": f_name,
                "lastname": l_name,
                "email": email,
                "username": username,
                "password": password,
                "weight": weight
            }
            database.child("users").child(username).set(data)
            res = '{"message":"' + 'success' + '"}'
            res = json.loads(res)
            return res
    except SQLAlchemyError as e:
        res = '{"message":"' + 'Error encountered ' + str(e.__dict__['orig']) + '"}'
        res = json.loads(res)
        return res

@app.route("/api/destinations_feedbacks", methods=["GET"]) #not firebase
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

def cell_auth(token):
    try:
        # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens/"+token+"/username.json"
        # user = json.load(urlopen(query_string))
        user = database.child("tokens").child(token).child("username").get().val()
        if user != None:
            return user
        else:
            return False
            # print(False)
    except:
        return False

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
        # db.execute("UPDATE users SET password = :password WHERE username = :username",
        #     {"username": username, "password": new_password})
        # db.commit()
        new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        database.child("users").child(username).update({"password": new_password})
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
        # db.execute("UPDATE users SET weight = :weight WHERE username = :username",
        #     {"username": username, "weight": new_weight})
        # db.commit()
        database.child("users").child(username).update({"weight": new_weight})
        res = '{"message":"' + 'success' + '"}'
        res = json.loads(res)
        return res
    except:
        res = '{"message":"' + 'error' + '"}'
        res = json.loads(res)
        return res

# @app.route("/api/test", methods=["GET"])
# def test():
#     username = request.args.get('username')
#     new_password = request.args.get('password')
#     new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
#     database.child("users").child(username).update({"password": new_password})

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
        # weight = db.execute("SELECT weight FROM public.users WHERE username = :username",
        #     {"username": username}).fetchone()['weight']
        # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/weight.json"
        # weight = int(json.load(urlopen(query_string)))
        weight = int(database.child("users").child(username).child("weight").get().val())
        entries = db.execute("SELECT date_trunc('day', timestamp)::date date, timestamp, lat, lng FROM public.trajectories WHERE date_trunc('day', timestamp) > CURRENT_DATE - 30 AND username = :username order by date desc",
            {"username": username})
        df = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
        # kalman_smoothing(array)
        # df_old = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
        df_new = df[['date', 'timestamp']]
        array = df.to_numpy()[:,2:]
        array = douglas_kalman_smoothing(array)
        df_new['lat'] = array[:,0].tolist()
        df_new['lng'] = array[:,1].tolist()
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
        print(e.message)
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
    # weight = db.execute("SELECT weight FROM public.users WHERE username = :username",
    #     {"username": username}).fetchone()['weight']
    # query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users/"+username+"/weight.json"
    # weight = int(json.load(urlopen(query_string)))
    weight = int(database.child("users").child(username).child("weight").get().val())
    # print(weight)
    entries = db.execute("SELECT date_trunc('day', timestamp)::date date, timestamp, lat, lng FROM public.trajectories WHERE date_trunc('day', timestamp) >= :startDate AND date_trunc('day', timestamp) <= :endDate AND username = :username order by date desc",
        {"username": username, "startDate":startDate, "endDate":endDate})
    df = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
    # print(df)
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
    except Exception as e:
        print(e)
    res = json.dumps({"message":"success","days":len(dateArray), "data":dateArray, "average":sum(dateArray)/len(dateArray), "total":sum(dateArray)})
    print(res)
    res = json.loads(res)
    return res


@app.route("/api/resetpassword", methods=["GET"])
def resetpassword():
    email = request.args.get('email')
    new_password = request.args.get('password')
    try:
        # db.execute("UPDATE users SET password = :password WHERE username = :username",
        #     {"username": username, "password": new_password})
        # db.commit()
        query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/users.json?orderBy=%22email%22&equalTo=%22" + email + "%22"
        reqs = json.load(urlopen(query_string))
        keys = [k  for  k in  reqs.keys()]
        username = keys[0]
        # print(username)
        if (username != None):
            new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            database.child("users").child(username).update({"password": new_password})
            res = '{"message":"' + 'success' + '"}'
            res = json.loads(res)
            return res
        else:
            res = '{"message":"' + 'incorrect email' + '"}'
            res = json.loads(res)
            return res
    except:
        res = '{"message":"' + 'error' + '"}'
        res = json.loads(res)
        return res


def douglas_kalman_smoothing(array):
    try:
        initial_state_mean = [array[0, 0],
                          0,
                          array[0, 1],
                          0]
        transition_matrix = [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]]
        observation_matrix = [[1, 0, 0, 0], [0, 0, 1, 0]]
        kf1 = KalmanFilter(transition_matrices = transition_matrix, observation_matrices = observation_matrix, initial_state_mean = initial_state_mean)
        kf1 = kf1.em(array, n_iter=5)
        # array = [tuple(row) for row in array]
        (smoothed_state_means, ) = kf1.smooth(array)
    except:
        pass
    return array
