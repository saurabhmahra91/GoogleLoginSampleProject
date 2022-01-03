# from flask import Flask, abort, session, request, make_response, jsonify
# from datetime import datetime
# from json import loads, dumps
# import requests
# from urllib.parse import urlparse,parse_qs
# from databases  import models
# import uuid
# from app import *




# @app.route("/time")
# def get_current_time():
#     return {"time": datetime.now()}


# @app.route("/loginWithGoogle", methods=["GET", "POST"])

# @app.route("/logout")
# def logout():
#     return {
#         "name":"saurabh",
#         "fuckYou": True
#     }

# @app.route("/")
# def index():
#     return "<h1>Index Page</h1>"



# @app.route("/auth/authToken",  methods=["POST", "GET"])
# def callback():
#     body=request.get_json()
#     callback_uri=body['callbackURL']
#     parsed_url=urlparse(callback_uri)
#     code=parse_qs(parsed_url.query)['code'][0]
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#     if str(app.config.get('FRONTEND_DOMAIN'))=='http://127.0.0.1:3000/':
#         token_url, headers, body = authclient.prepare_token_request(
#                                 token_endpoint,
#                                 authorization_response=callback_uri,
#                                 redirect_url='http://localhost:3000/auth/authToken',
#                                 code=code
#                             )
#     else:
#         token_url, headers, body = authclient.prepare_token_request(
#                                 token_endpoint,
#                                 authorization_response=callback_uri,
#                                 redirect_url=str(app.config.get('FRONTEND_DOMAIN'))+'auth/authToken',
#                                 code=code
#                             )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=( app.config.get('GO_AUTH_CLIENT'), app.config.get('GO_AUTH_SECRET')),
#     )
#     authclient.parse_request_body_response(dumps(token_response.json()))
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = authclient.add_token(userinfo_endpoint)    
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#     print(userinfo_response.content)
#     if userinfo_response.json().get("email_verified"):
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["name"]
    
#         if User.objects(emailID=users_email).first():
#             #Existing User
#             user=User.objects(emailID=users_email).first()
#             profile=Profile.objects.get(userID=User.objects(emailID=users_email).first().userID)
#             token=user.encode_signin_token()
#             return make_response(jsonify({'token':token,'user':User.objects.get(emailID=users_email),'profile':profile,'sucess':True}))
#         else:
#             #New User
#             u=User()
#             u.firstName=userinfo_response.json()["given_name"]
#             try:
#                 u.lastName=userinfo_response.json()["family_name"]
#             except:
#                 u.lastName=''
#             u.emailID=users_email
#             u.password="LOGGEDINWITHGOOGLE"
#             u.hash_password()
#             u.confirmPassword="LOGGEDINWITHGOOGLE"
#             u.userID=uuid.uuid4()
#             u.isVerified=True
#             u.save()
#             p=Profile()
#             p.randomize()
#             p.profileID=uuid.uuid4()
#             p.userID=u.userID
#             p.profilePicImageURL=picture
#             p.profileName=userinfo_response.json()["name"]
#             p.profileUserName=u.emailID.split('@')[0].replace('.','_')
#             p.save()
#             token=u.encode_signin_token()
#             return make_response(jsonify({'token':token,'user':u,'profile':p,'success':1}))                
#     else:
#         return make_response(jsonify({"Message":"User email not available or not verified by Google."}))



