import time
from flask import Flask, abort, session, redirect, request
from google_auth_oauthlib.flow import Flow
import os
from dotenv import load_dotenv
import requests
from google.oauth2 import id_token
import google.auth.transport.requests#, cachecontrol
import requests
from pip._vendor import cachecontrol


app = Flask("Google Login Sample App")
app.secret_key = "saurabhmahrasecretkey" # to encrypt/decrypt session data

#loading env variables
load_dotenv()
client_id=os.getenv("client_id")
# client_secret=os.getenv("client_secret")
# secret_key=os.getenv("secret_key")


# internally trying to make an attempt to open a file with name client_Secret as json. Download this file from google cloud console and save it in same directory as this file
client_secret_file = os.path.join(os.getcwd(), "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# allow google verification at http too (default behavior is to support https only)  
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper

@app.route("/login")
def login():

    #state is a security feature. We create a random state before login and obtain a state from google after login (see the callback route), if both match we're good to go. 
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    print("auth url is-->", authorization_url)
    print("state is-->", state)
    return redirect(authorization_url)

@app.route("/logout")
def logout():
    pass

@app.route("/prohibited")
@login_required
def prohibited():
    return "prohibited area"

@app.route("/")
def index():
    return "<h1>Index Page</h1>"


@app.route("/callback")
def callback():
    print("HELLOOOOOOOOOOOOOOOOOOO")
    flow.fetch_token(authorization_response=request.url) #flask request acts like a "global variable"
    if not session['state'] == request.args["state"]: #to stop csrf attacks
        abort(500)
    
    # if flow.fetch_token worked fine, we will obtain the user credentials through flow.credentials 
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    
    #for some reasons that i dont know, I was getting an error saying token used too early. I am assuming this is because I am running the backend on the same server and there might be some time offset b/n my computer and google's api server. This should not be the case in production environment!!. Try once with time.sleep() removed in your local machine.
    # time.sleep(5)


    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=client_id,
    )
    return id_info

if __name__ == "__main__":
    app.run(debug=True)
