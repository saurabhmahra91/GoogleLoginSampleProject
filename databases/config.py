from pymongo import MongoClient
client = MongoClient("localhost", 27017, maxPoolSize=50)
db = client.users
user_collection = db.users

print(user_collection.find_one({"name":"saurabh"}))
user_collection.update_one({"name":"saurabh"}, {"$set":{"name":"kshitij"}})
print(type(user_collection.find_one({"name":"kshitij"})))
