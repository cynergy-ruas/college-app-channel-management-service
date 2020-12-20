from fastapi import FastAPI,APIRouter,HTTPException
from app.database.schema import Channel
from app.database.update_modal import Change_channel
from bson.objectid import ObjectId
channelsRouter = APIRouter() 
from app.config.config import channel_DB
from bson import ObjectId
import datetime

def fetch_channels() -> list:
    """
    Args : none

    Fetching all the channels from the database

    Return type : List
    """
    channels_list = []
    query = channel_DB().find({"type":"public"})
    for each_channel in query:
        channels_list.append(Channel(**each_channel))
    return channels_list

def fetch_channel(id) -> dict:
    """
    fetch details of a channel with the given _id

    Args:
        id (str): id created by the mongoDB

    Returns:
        channel_details[dict]: [the details of the channel requested]
    """
    channel_details = dict(channel_DB().find_one({"_id": ObjectId(id)}))
    channel_details.pop("_id")
    return channel_details

def create_channel(channel: Channel) -> Channel:
    """
    Args : channel -> Channel

    creates new channel in the database

    return type : list

    """
    if hasattr(channel, 'id'):
        delattr(channel, 'id')
    channel.created_at= datetime.datetime.now()
    newChannel = channel_DB().insert_one(channel.dict(by_alias=True))
    channel.id = newChannel.inserted_id
    return {'channel': channel}    

def update_channel(id: str, new_data: Change_channel) -> Channel:
    check_channel = channel_DB().find_one({"_id": ObjectId(id)})
    #need to add a checking logic if the channel exist or not using above request
    updated_channel = channel_DB().update_one({"_id": ObjectId(id)}, {"$set": dict(new_data)})
    return "channel is updated"

#custom exception 
#https://www.programiz.com/python-programming/user-defined-exception
class Error(Exception):
    """Base class for other exceptions"""
    pass

class RandomError(Error):
    """Raised when the channel is not found"""
    pass

def remove_channel(id: str):
    """
    Args:
    id -> string

    deletes a channel from the database

    return type: string
    """
    try:
        delChannel=channel_DB().delete_one({"_id":ObjectId(id)})
        if delChannel.deleted_count==0:
            raise  RandomError
        else:
            return("sueach_channelessfully deleted")

    except RandomError:
        return "channel not found"      

        