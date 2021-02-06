import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGO_URL = os.environ.get("MONGODB_URI")
DB_NAME = "app-channel"
CHANNEL_COLL = "channels"
MEMBERSHIP_COLL = "membership"
