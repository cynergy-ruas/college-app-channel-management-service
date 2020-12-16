from fastapi import APIRouter,HTTPException
from bson import ObjectId
from app.database.schema import Channel
from app.services.controller import fetch_channel, create_channel, remove_channel
channelsRouter = APIRouter()

@channelsRouter.get('/channels/all')
async def get_Channel():
    """
    Endpoint to get all the channels

    Args: none

    This endpoint is used to get all the channels from database and 
    is handeled by controller function fetch_channel() 

    Return type: list
    """
    return fetch_channel()

@channelsRouter.post('/channels/create')
async def post_channel(channel: Channel):
    """
    Args : channel -> Channel

    This endpoint is used to create a new channel in the database
    is handeled by controller function create_channel()

    return type : list
    """
    return create_channel(channel)

@channelsRouter.delete("/channels/delete/{id}", response_description="Delete channel")
async def delete_channel(id: str):
    """
    Args: 
    id -> String 
    
    This route is used to delete a channel from the database and is handled by controller 
    function remove_message() from controller.py
    
    Return Type : String
    
    """
    return remove_channel(id)


