import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")
CHANNEL_DB = "channels"
MEMBERSHIP_DB = "membership"
