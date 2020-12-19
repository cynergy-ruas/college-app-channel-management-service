import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

user_name = os.environ.get('MONGO_USER')
password = os.environ.get('MONGO_PASSWORD')
DB_NAME= os.environ.get('MONGO_DB')
print(user_name,password,DB_NAME)
MONGODB_URI ="mongodb+srv://"+user_name+":"+password+"@ruas-app.63rrs.mongodb.net/"+DB_NAME+"?retryWrites=true&w=majority"
PORT = 8000
#channels
CHANNEL_DB = "channels"
MEMBERSHIP_DB = "membership" 
