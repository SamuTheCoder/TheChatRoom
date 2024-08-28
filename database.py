from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["the_chatroom_db"]

users_collection = db["users"]
messages_collection = db["messages"]
sessions_collection = db["sessions"]

def create_user(username):
    user = users_collection.find_one({"username": username})
    if not user:
        user_id = users_collection.insert_one({
            "username": username,
            "created_at": datetime.utcnow()
        }).inserted_id
        return user_id
    return user["_id"]

def create_message(user_id, username, message):
    messages_collection.insert_one({
        "user_id":  user_id,
        "username": username,
        "message": message,
        "created_at": datetime.utcnow()
    })
    
def get_history(limit=100):
    return list(messages_collection.find().sort("created_at", -1).limit(limit))

def create_session(username):
    session = sessions_collection.find_one({"username": username})
    if session:
        return False
    
    session_id = sessions_collection.insert_one({
        "username": username,
        "created_at": datetime.utcnow()
    })
    return session_id

def end_session(username):
    sessions_collection.delete_one({"username": username})


