from bson import ObjectId
from app.database.__init__ import MongoDB
from app.models.membership_model import Membership
from app.models.channel_model import Channel

def find_channels_all(query: dict):
    """Function to find channels using query condition

    Args: 
        query(dict) : the query being used to find channels 

    Returns:
        (pymongo.cursor.Cursor): it is used in channel_service to loop through the channels
    """
    list_of_channels = MongoDB.channel_db().find(query)
    return list_of_channels



def find_channel(id: str):
    """Function to find a channel using id

    Args:
        id (str): channel id

    Returns:
        (dict): dict of all the channel details
        (None): if channel is not found
    """
    channel_details = MongoDB.channel_db().find_one({"_id": ObjectId(id)})
    return channel_details


def insert_channel(channel: Channel):
    """Function to insert a channel into db

    Args:
        channel (Channel): dict containing details of channel to be created

    Returns:
        new_channel(class 'pymongo.results.InsertOneResult)
    """

    new_channel = MongoDB.channel_db().insert_one(channel.dict(by_alias=True))
    return new_channel


def update_channelinfo(id: str, UPDATE_data: dict):
    """Function to update a channel in db

    Args:
        id (str): description
        UPDATE_data (dict): description

    Returns:
        (type): description
    """
    update_channel = MongoDB.channel_db().update_one(
        {"_id": ObjectId(id)}, {"$set": UPDATE_data}
    )
    return update_channel


def delete_channel(id: str):
    """Function to delete a channel in db

    Args:
        id (str): description

    Returns:
        (type): description
    """
    delChannel = MongoDB.channel_db().delete_one({"_id": ObjectId(id)})
    return delChannel


def find_membership(user_id: str):
    """Function to find a membership of user in db

    Args:
        user_id(str): description

    Returns:
        user_details(dict) : Membership of the user from membership db 
    """
    user_details = MongoDB.membership_db().find_one({"_id": ObjectId(user_id)})
    return user_details


def insert_membership(user_id: str, id: str) -> dict:
    """Function to insert a membership of user into db

    Args:
        user_id(str): user id
        id(str) : channel id

    Returns:
        membership(dict): dict of type Membership from app.models.membership_model
    """
    membership = Membership(channel_id=[id])
    membership.id = ObjectId(user_id)
    newuser = MongoDB.membership_db().insert_one(membership.dict(by_alias=True))
    membership.id = newuser.inserted_id
    return membership


def update_membership(user_id: str, new_data: dict):
    """Function to update a membership of user in db

    Args:
        user_id (str): description
        new_data (dict): description

    Returns:
        (class 'pymongo.results.UpdateResult'): sent by mongodb 
    """
    updating_membership = MongoDB.membership_db().update_one(
        {"_id": ObjectId(user_id)}, {"$set": new_data}
    )
    return updating_membership