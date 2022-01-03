import secrets
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
import string    
import secrets
import random

from pymongo import MongoClient
db = MongoClient("localhost", 27017, maxPoolSize=50)

class User(db.Document):
    userID = db.UUIDField(required=True,binary=False)
    firstName = db.StringField(required=True)
    lastName=db.StringField(required=True)
    emailID = db.EmailField(required=True,unique=True)
    password = db.StringField(required=True,min_length=6)
    confirmPassword = db.StringField(required=False,min_length=6)
    role=db.IntField(default=0,required=False)
    isVerified = db.BooleanField(default=False,required=False)
    def generate_password(self,num=10):
        res = ''.join(secrets.choice(string.ascii_letters + string.punctuation) for x in range(num))  
        self.password=res
        self.hash_password()
        return res 
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self,password):
        return check_password_hash(self.password,password)
    def encode_signin_token(self):
        profile=Profile.objects.get(userID=self.userID)
        payload={
            'emailID':self.emailID,
            'iat':datetime.datetime.utcnow(),
            'profileID':str(profile.profileID)
        }
        return jwt.encode(payload,'SECRET_KEY',algorithm='HS256')
        
    def encode_auth_token(self):
        payload={
            'emailID':self.emailID,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(days=0,minutes=30,seconds=30),
            'iat':datetime.datetime.utcnow()
        }
        return jwt.encode(payload,'SECRET_KEY',algorithm='HS256')
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload=jwt.decode(auth_token,'SECRET_KEY',algorithms='HS256')
            print("Executed")
            return payload['emailID']
        except jwt.ExpiredSignatureError:
            return 'Singnature Expired.Please Signup Again'
        except jwt.InvalidTokenError:
            return 'Invalid Token'

class Profile(db.Document):    
    profileID=db.UUIDField(required=True,binary=False)
    userID=db.UUIDField(required=True,binary=False)
    profilePicImageURL=db.URLField(required=False)
    profileBannerImageURL=db.URLField(required=False)
    profileGender=db.StringField(required=False,max_length=10)
    profileName=db.StringField(required=False,max_length=100)
    profileUserName=db.StringField(required=True,unique=True,max_lenght=15)
    profileBio=db.StringField(required=False,max_length=300)
    Followers=db.ListField(db.UUIDField(required=True,binary=False),required=False,default=[])
    Following=db.ListField(db.UUIDField(required=True,binary=False),required=False,default=[])
    FollowersCount=db.IntField(required=False,default=0)
    FollowingCount=db.IntField(required=False,default=0)
    interests=db.ListField(db.StringField(max_length=50),required=False,default=[])
    # getBlogs from blog api
    profileWebsiteURL=db.URLField(required=False)
    profileTimestamp=db.DateTimeField(required=False,default=datetime.datetime.utcnow)
# Random photo selector
    def randomize(self):
        banner = ["https://res.cloudinary.com/dd8470vy4/image/upload/v1628924597/default_banner5_vozcng.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1628924597/dafault_banner1_t1jtqd.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1628924597/default_banner2_cbkpwx.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1628924597/default_banner4_fsgrie.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1628924597/default_banner6_lxhjrl.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1628924597/default_banner3_uyxaii.jpg"]
        male = ["https://res.cloudinary.com/dd8470vy4/image/upload/v1628924598/Profile_Pic_male_mg0kie.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1629308403/male_profile_pic3_f8mtlr.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1629308402/male_profile_pic2_gcafhp.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1629308402/male_profile_pic4_mnjejq.jpg"]
        female = ["https://res.cloudinary.com/dd8470vy4/image/upload/v1628924598/Profile_Pic_Female_hwkfwv.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1629308402/female_profile_pic2_mqaiuh.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1629308402/female_profile_pic3_oxfaio.jpg","https://res.cloudinary.com/dd8470vy4/image/upload/v1629308402/female_profile_pic4_vkmvfj.jpg"]
        banner_ = random.randint(0,len(banner)-1)
        male_ = random.randint(0,len(male)-1)
        female_ = random.randint(0,len(female)-1)
        self.profileBannerImageURL=banner[banner_]
        self.profilePicImageURL=male[male_]
