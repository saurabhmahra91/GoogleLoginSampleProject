from urllib.parse import urlparse, parse_qs
from datetime import datetime
from flask import Flask, abort, session, request, make_response, jsonify
from flask import Flask
from flask.json import dumps
import jwt
from jwt.exceptions import InvalidSignatureError
import requests
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient
import os
from dotenv import load_dotenv
from werkzeug.utils import redirect
from functools import wraps
from json import loads
from bson import json_util


app = Flask("Google Login Sample App")
# by default two servers running and communicating with each other is not allowed. this is to override it.
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
authclient = WebApplicationClient(os.getenv("client_id"))

# to encrypt/decrypt session data. It's not required if you're not using sessions
app.secret_key = "saurabhmahrasecretkey"

# loading env variables
load_dotenv()
client_id = os.getenv("client_id")
# client_secret=os.getenv("client_secret")
# secret_key=os.getenv("secret_key")


# internally trying to make an attempt to open a file with name client_Secret as json. Download this file from google cloud console and save it in same directory as this file
client_secret_file = os.path.join(os.getcwd(), "client_secret.json")


# allow google verification at http too (default behavior is to support https only)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return {"message": "missing user token"}, 401
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithm="HS256")
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, maxPoolSize=50)
            db = client.users
            user_collection = db.users 
            user = user_collection.find_one({"emailID":data["emailID"]})
        except InvalidSignatureError:
            return {"message": "invalid user token"}, 401
        except:
            return {"message": "authenticity of the user could not be verified"}, 401

        return function(user, *args, **kwargs)
    return decorated


@app.route("/time")
def get_current_time():
    return {"time": datetime.now()}


@app.route("/me")
@token_required
def get_logged_in_name(user):
    return {"email": user.emailID}


@app.route("/logout")
def logout():
    return {
        "name": "saurabh",
        "fuckYou": True
    }


@app.route("/login")
def login():
    # DO  NOT USE @token_required FOR THIS ROUTE
    # FIND THE USER ACCORDING TO THE PROVIDED INFO
    # ENCODE THE USER, AND OBTAIN A TOKEN. SET A TOKEN EXPIRATION TIME, SAY 5 DAYS
    # DECODE THE TOKEN YOU JUST CREATED
    # SEND THIS DECODED TOKEN BACK TO THE LOGGEDINUSER
    return {
        "name": "saurabh",
        "loggedIn": True
    }


@app.route("/",  methods=["GET", "POST"])
def index():
    return "<h1>Index Page</h1>"


@app.route("/getLoggedInUser",  methods=["GET"])
def get_logged_in_user():
    if session["email"]:
        return {"name": "Saurabh", "loggedIn": True}
    else:
        return {"loggedIn": False}



@app.route("/googleToken",  methods=["POST"])
def googleLogin():
    # To verify once the tokens, do not send the userinfo with request
    google_profile = request.get_json(silent=True)["googleData"]['profileObj']
    email = google_profile["email"]
    familyName = google_profile["familyName"]
    givenName = google_profile["givenName"]
    googleId = google_profile["googleId"]
    imageUrl = google_profile["imageUrl"]
    # INSERT THE USER INTO DATABASE AND CREATE A TOKEN
    # FIND THE USER ACCORDING TO THE PROVIDED INFO
    # ENCODE THE USER, AND OBTAIN A TOKEN. SET A TOKEN EXPIRATION TIME, SAY 5 DAYS
    # DECODE THE TOKEN YOU JUST CREATED
    # SEND THIS DECODED TOKEN BACK TO THE LOGGEDINUSER
    from pymongo import MongoClient
    client = MongoClient("localhost", 27017, maxPoolSize=50)
    db = client.users
    user_collection = db.users
    print("client", client, type(client))
    print("db", db, type(db))
    print("user_collection", user_collection, type(user_collection))
    a = user_collection.find({})
    print("type(a)=",type(a))
    print("type(user_collection.find())=",user_collection.find({}))
    for i in a:
        print(i)
    # print(a = user_collection.find({}))
    # print(db)
    # print(client)
    results = list(user_collection.find({"emailID": email}))
    if len(results) > 0:
        # EXISTING USER
        found_user = user_collection.find_one({"emailID": email})
        token = jwt.encode(loads(json_util.dumps(found_user)), os.getenv("secret_key"), algorithm='HS256')
        return {"token": token}
    else:
        # NEW USER
        #TODO Check for email verified
        new_user = {
            "firstName": givenName,
            "emailID": email,
            "lastName":familyName
        }
        user_collection.insert_one(new_user)
        token = jwt.encode(loads(json_util.dumps(new_user)), os.getenv("secret_key"), algorithm='HS256')
        return {"token": token}

if __name__ == "__main__":
    app.run(debug=True)
