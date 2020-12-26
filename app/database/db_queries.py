from bson import ObjectId
from app.config.config import channel_DB, membership_DB
from app.database.membership_modal import Membership
from app.database.schema import Channel

def find_channels_all(query: dict):
    """Function to find channels using query condition

    Args: 
        query[dict] : the query being used to find channels 

    Returns:
        [pymongo.cursor.Cursor]: [it is used in controller to loop through the channels]
    """
    list_of_channels = channel_DB().find(query)
    return list_of_channels



def find_channel(id: str):
    """Function to find a channel using id

    Args:
        id ([str]): [channel id]

    Returns:
        [dict]: [dict of all the channel details]
        [None]: [if channel is not found]
    """
    channel_details = channel_DB().find_one({"_id": ObjectId(id)})
    return channel_details


def insert_channel(channel: Channel):
    """Function to insert a channel into db

    Args:
        channel (Channel): [dict containing details of channel to be created]

    Returns:
        new_channel[class 'pymongo.results.InsertOneResult]
    """

    new_channel = channel_DB().insert_one(channel.dict(by_alias=True))
    return new_channel


def update_channelinfo(id: str, UPDATE_data: dict):
    """Function to update a channel in db

    Args:
        id (str): [description]
        UPDATE_data (dict): [description]

    Returns:
        [type]: [description]
    """
    update_channel = channel_DB().update_one(
        {"_id": ObjectId(id)}, {"$set": UPDATE_data}
    )
    return update_channel


def delete_channel(id: str):
    """Function to delete a channel in db

    Args:
        id (str): [description]

    Returns:
        [type]: [description]
    """
    delChannel = channel_DB().delete_one({"_id": ObjectId(id)})
    return delChannel


def find_membership(user_id: str):
    """Function to find a membership of user in db

    Args:
        user_id (str): [description]

    Returns:
        [type]: [description]
    """
    user_details = membership_DB().find_one({"_id": ObjectId(user_id)})
    return user_details


def insert_membership(user_id: str, id: str) -> dict:
    """Function to insert a membership of user into db

    Args:
        user_id[str]: [user id]
        id[str] : [channel id]

    Returns:
        membership[dict]: [dict of type Membership from app.database.membership_modal]
    """
    membership = Membership(channel_id=[id])
    membership.id = ObjectId(user_id)
    newuser = membership_DB().insert_one(membership.dict(by_alias=True))
    membership.id = newuser.inserted_id
    return membership


def update_membership(user_id: str, new_data: dict):
    """Function to update a membership of user in db

    Args:
        user_id (str): [description]
        new_data (dict): [description]

    Returns:
        [type]: [description]
    """
    updating_membership = membership_DB().update_one(
        {"_id": ObjectId(user_id)}, {"$set": new_data}
    )
    return updating_membership