from fastapi import APIRouter,HTTPException
from bson import ObjectId
from app.database.schema import Channel
# , Change_channel
from app.services.controller import fetch_channels, create_channel, remove_channel, fetch_channel
# , update_channel
channelsRouter = APIRouter()

@channelsRouter.get('/channels/all')
async def get_Channels():
    """
    Endpoint to get all the channels

    Args: none

    This endpoint is used to get all the channels from database and 
    is handeled by controller function fetch_channel() 

    Return type: list
    """
    return fetch_channels()

@channelsRouter.get('/channels/info/{id}')
async def getChannel(id: str):
    """
    Endpoint to get info of a channel

    Args:
        id (str): [channel_id of channel whose info is required]

    Returns:
        [type]: [description]
    """
    return fetch_channel(id)

@channelsRouter.post('/channels/create')
async def post_channel(channel: Channel):
    """
    Args : channel -> Channel

    This endpoint is used to create a new channel in the database
    is handeled by controller function create_channel()

    return type : Channel
    """
    return create_channel(channel)

# @channelsRouter.post("/channels/info/{id}", response_description="update channel")
# async def edit_channel(id: str, new_data: Change_channel):
#     """
#     endpoint to update channel info

#     Args:
#         id (str): [channel id which is being edited]

#     Returns:
#         Channel [dict]: [updated channel info]
#     """
#     return update_channel(id, new_data)

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


