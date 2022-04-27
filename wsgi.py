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

if __name__ == "__main__":
    token = "cd1f0d7032aacfad6c61e04bc0e11a03"
    query_string = "https://engo-651-final-project-default-rtdb.firebaseio.com/tokens/"+token+"/username.json"
    reqs = json.load(urlopen(query_string))
    print(reqs)
