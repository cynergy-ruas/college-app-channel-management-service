from fastapi import APIRouter,HTTPException
from bson import ObjectId
from app.database.schema import Channel
from app.database.update_modal import Change_channel
from app.database.membership_modal import Membership
from app.services.controller import (fetch_channels, create_channel, remove_channel,
                                        fetch_channel, update_channel, join_user)
from app.services.errorCustom import RuasAppExceptions
channelsRouter = APIRouter()

# channel endpoints
@channelsRouter.get('/channels/all')
async def get_Channels():
    """
    Endpoint to get all the channels

    Args: none

    This endpoint is used to get all the channels from database and 
    is handeled by controller function fetch_channel() 

    Return type: list
    """
    response = fetch_channels()
    if type(response)== RuasAppExceptions:
        raise HTTPException(status_code=404, detail=str(response))
    else:
        return response

@channelsRouter.get('/channels/info/{id}')
async def getChannel(id: str):
    """
    Endpoint to get info of a channel

    Args:
        id (str): [channel_id of channel whose info is required]

    Returns:
        [type]: [description]
    """
    response = fetch_channel(id)
    if type(response)== RuasAppExceptions:
        raise HTTPException(status_code=404, detail=str(response))
    else:
        return response


@channelsRouter.post('/channels/create/{user_id}')
async def post_channel(user_id: str, channel: Channel):
    """
    Args : channel -> Channel

    This endpoint is used to create a new channel in the database
    is handeled by controller function create_channel()

    return type : Channel
    """

    response = create_channel(user_id, channel)
    if type(response)== RuasAppExceptions:
        raise HTTPException(status_code=485, detail=str(response))
    else:
        return response

@channelsRouter.post("/channels/info/{id}", response_description="update channel")
async def edit_channel(id: str, new_data: Change_channel):
    """
    endpoint to update channel info

    Args:
        id (str): [channel id which is being edited]

    Returns:
        Channel [dict]: [updated channel info]
    """
    response = update_channel(id, new_data)
    if type(response)== RuasAppExceptions:
        raise HTTPException(status_code=404, detail=str(response))
    else:
        return response
    

@channelsRouter.delete("/channels/delete/{id}", response_description="Delete channel")
async def delete_channel(id: str, user_data: dict):
    """
    Args: 
    id -> String 

    This route is used to delete a channel from the database and is handled by controller 
    function remove_message() from controller.py
    
    Return Type : String
    
    """
    response = remove_channel(id, user_data['user_id'])
    if type(response)== RuasAppExceptions:
        raise HTTPException(status_code=404, detail=str(response))
    else:
        return response 


#membership endpoints
@channelsRouter.post('/channels/join/{id}')
async def add_user_toChannel( id: str, user_data: dict ):
    response = join_user(id, user_data)
    if type(response)== RuasAppExceptions:
        raise HTTPException(status_code=485, detail=str(response))
    else:
        return response

