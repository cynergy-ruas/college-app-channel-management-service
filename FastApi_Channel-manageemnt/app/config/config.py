from pymongo import MongoClient
from app.config.settings import MONGODB_URI,CHANNEL_DB,DB_NAME,PORT,MEMBERSHIP_DB 

#creating a connection with MongoClient and its attributes from settings.py
CLIENT = MongoClient(MONGODB_URI,PORT)
#assigning database to a variable db  
DB = CLIENT[DB_NAME]

def channel_DB():
    return DB[CHANNEL_DB]

def membership_DB():
    return DB[MEMBERSHIP_DB]