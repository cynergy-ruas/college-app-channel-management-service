from fastapi import FastAPI,APIRouter,HTTPException
from app.database.schema import Channel
from bson.objectid import ObjectId
channelsRouter = APIRouter() 
from app.config.config import channel_DB
from bson import ObjectId

def fetch_channel():
    """
    Args : none

    Fetching all the channels from the database

    Return type : List
    """
    channels_list = []
    for channel in channel_DB().find():
        each_channel=dict(list(Channel(**channel)))
        if (each_channel['type']=="public"):
            channels_list.append(Channel(**channel))
    return {'channels': channels_list}

def create_channel(channel: Channel) -> Channel:
    """
    Args : channel -> Channel

    creates new channel in the database

    return type : list

    """
    if hasattr(channel, 'id'):
        delattr(channel, 'id')
    newChannel = channel_DB().insert_one(channel.dict(by_alias=True))
    channel.id = newChannel.inserted_id
    return {'channel': channel}    


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
        print("Channel not found")
        return "channel not found"      

        