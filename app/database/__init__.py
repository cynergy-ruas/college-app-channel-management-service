from app.configs import DB_NAME, MONGO_URL, MEMBERSHIP_DB, CHANNEL_DB
from pymongo import MongoClient


class MongoDB:
    """
    This Class is used the Handle all the Settings for MongoDB Stuff
    """

    _instance = None

    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DB_NAME]

    @staticmethod
    def get_instance():
        """
        This Function is used to get the instance of the MongoDB Class
        Returns:
            This Returns the object of the MongoDB Class
        """
        if MongoDB._instance is None:
            MongoDB._instance = MongoDB()
        return MongoDB._instance

    @staticmethod
    def get_database():
        """
        This Function is used to get the database
        Returns:
             This Returns the Database
        """
        return MongoDB.get_instance().db

    @staticmethod
    def channel_db():
        """
        This Function is used to get the collection
        Returns:
             This Returns the collection
        """

        return MongoDB.get_database()[CHANNEL_DB]

    @staticmethod
    def membership_db():
        """
        This Function is used to get the collection
        Returns:
             This Returns the collection
        """

        return MongoDB.get_database()[MEMBERSHIP_DB]