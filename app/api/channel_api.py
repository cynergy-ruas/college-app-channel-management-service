from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.models.channel_model import Channel
from app.models.update_model_channel import Change_channel
from app.models.membership_model import Membership
from app.services.channel_service import (
    fetch_channels,
    create_channel,
    remove_channel,
    fetch_user_membership,
    fetch_channel,
    user_leave,
    update_channel,
    join_user,
)

from app.utils.err_codes import Code

# V1 add_admin,
from app.utils.err_custom import ReturnExceptions

channels_router = APIRouter()

# channel endpoints
@channels_router.get(
    "/channels/all",
    response_description="list of all public channels with details in the db",
)
async def get_channels():
    """
    Endpoint to get all the channels

    Returns:
        channels(list): list of channel(dict)
    """
    try:
        response = fetch_channels()
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.get(
    "/channels/user", response_description="list of user's membership channels' id"
)
async def get_user_channels(app_user_id: Optional[str] = Header(None)):
    """
    Endpoint to get user_channels

    Args:
        app_user_id(str): "user id to check in membership db"

    Returns:
        user_channels(list): list of all the channels user is member
    """
    try:
        response = fetch_user_membership(app_user_id)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.get(
    "/channels/info", response_description="dict of requested channel's details"
)
async def get_channel_info(app_channel_id: Optional[str] = Header(None)):
    """
    Endpoint to get info of a channel

    Args:
         app_channel_id(str): channel_id of channel whose info is required

    Returns:
         channel_info(dict): details of the channel
    """
    try:
        response = fetch_channel(app_channel_id)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post(
    "/channels/create", response_description="dict of created channel's details"
)
async def post_channel(channel: Channel, app_user_id: Optional[str] = Header(None)):
    """
    Endpoint to create a new channel in the database

    Args:
        app_user_id(str) : id of user creating the channel
        channel(Channel) : channel details recieved from body

    Returns:
        channel (dict): created channel is returned
    """
    try:
        response = create_channel(app_user_id, channel)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post(
    "/channels/info", response_description="dict of updated channel's details"
)
async def edit_channel(
    new_data: Change_channel, app_channel_id: Optional[str] = Header(None)
):
    """
    Endpoint to update info of a channel

    Args:
        app_channel_id(str): channel's id which is being edited

    Returns:
        Channel (dict): updated channel info
    """
    try:
        response = update_channel(app_channel_id, new_data)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


# user_data also should be retrieved from header
@channels_router.post(
    "/channels/join",
    response_description="dict of user's membership details or user added",
)
async def add_user_to_channel(
    user_data: dict, app_channel_id: Optional[str] = Header(None)
):
    """
    Endpoint to add user to a channel

    Args:
        app_channel_id(str): channel's id user is requesting to join
        user_data (dict): user_id(str) is user being added,
                            req_user(str): user sending req(may or may not be admin)

    Returns:
        membership(dict): membership of user is returned
    """
    try:
        response = join_user(app_channel_id, user_data)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post(
    "/channels/leave",
    response_description="list of user's updated membership channels' ids",
)
async def leave_channel(
    app_user_id: Optional[str] = Header(None),
    app_channel_id: Optional[str] = Header(None),
):
    """
    Endpoint to for an user to leave a channel

    Args:
        app_channel_id(str): channel's id user is requesting to leave
        app_user_id(str): user leaving channel

    Returns:
        membership channels(list): list of channel_id in user membership after updating it
    """
    try:
        response = user_leave(app_channel_id, app_user_id)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.delete(
    "/channels/delete", response_description="deleted channel details is returned"
)
async def delete_channel(
    app_user_id: Optional[str] = Header(None),
    app_channel_id: Optional[str] = Header(None),
):
    """
    Endpoint to delete a channel

    Args:
        app_channel_id(str): channel_id
        app_user_id(str): user sending req(may or may not be owner)

    Returns:
        deleted_channel(dict): details of channel deleted(may be useful if we are gonna make an undo functionality)
    """
    try:
        response = remove_channel(app_channel_id, app_user_id)
        return response
    except ReturnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


# @channels_router.post('/channels/admin/{id}/{user_id}')
# async def make_admin( id: str, user_id: str, user_data: dict):
#     try:
#         response = add_admin(id, user_id, user_data)
#         return response
#     except ReturnExceptions as err:
#         raise HTTPException(status_code=Code.error_enum_http[err.error_code], detail=str(err))