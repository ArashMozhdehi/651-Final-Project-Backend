from application import app
from firebase import firebase
import json
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
from urllib.request import urlopen
from pykalman import KalmanFilter


DATABASE_URL = "postgresql://icnbjzbcznpgfp:a952b3bdc51644c4fb224f2dd8a7c358bc6a6e2fcf80a57a5e0d4956808d02a6@ec2-54-226-18-238.compute-1.amazonaws.com:5432/dbeqq9egku7fm5"
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def kalman_smoothing(array):
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


if __name__ == "__main__":
    entries = db.execute("SELECT date_trunc('day', timestamp)::date date, timestamp, lat, lng FROM public.trajectories WHERE date_trunc('day', timestamp) > CURRENT_DATE - 30 AND username = :username order by date desc",
        {"username": "amozhdehi"})
    df_old = pd.DataFrame(entries, columns=['date', 'timestamp', 'lat', 'lng'])
    df = df_old[['date', 'timestamp']]
    array = df_old.to_numpy()[:,2:]
    array = kalman_smoothing(array)
    df['lat'] = array[:,0]
    df['lng'] = array[:,1]
    print(array.shape)
    print(df.to_numpy().shape)
