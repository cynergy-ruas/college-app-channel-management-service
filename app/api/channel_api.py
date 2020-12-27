from fastapi import APIRouter, HTTPException
from app.database.schema import Channel
from app.database.update_modal_channel import Change_channel
from app.database.membership_modal import Membership
from app.services.controller import (
    fetch_channels,
    create_channel,
    remove_channel,
    fetch_user_membership,
    fetch_channel,
    user_leave,
    update_channel,
    join_user
)

from app.config.err_codes import Code
# V1 add_admin,
from app.services.error_custom import returnExceptions

channels_router = APIRouter()

# channel endpoints
@channels_router.get("/channels/all")
async def get_channels():
    """
    Endpoint to get all the channels

    Raises:
        HTTPException: ["All channels are private",
                        or "Oops! Unexpected mongodb error occurred"]

    Returns:
        channels[list]: [list of channel[dict]]
    """
    try:
        response = fetch_channels()
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.get(
    "/channels/user/{user_id}",
    response_description="list of channels an user is subscribed to",
)
async def get_user_channels(user_id: str):
    """
    Endpoint to get user_channels

    Args:
        user_id[str]: ["user id to check in membership db"]

    Raises:
        HTTPException: ["User Not Found "
                        or "Oops! Unexpected mongodb error occurred"]

    Returns:
        user_channels[list]: [list of all the channels user is member]
    """
    try:
        response = fetch_user_membership(user_id)
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.get("/channels/info/{id}")
async def get_channel_info(id: str):
    """
    Endpoint to get info of a channel

    Args:
         id (str): [channel_id of channel whose info is required]

    Raises:
        HTTPException: ["Oops! Unexpected mongodb error occurred" or
                        "channel Not Found"]

    Returns:
         channel_info[dict]: [details of the channel]
    """
    try:
        response = fetch_channel(id)
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post("/channels/create/{user_id}")
async def post_channel(user_id: str, channel: Channel):
    """
    Endpoint to create a new channel in the database

    Args:
        user_id[str] : [for dev purpose, need to get this from header]
        channel[Channel] : [channel details recieved from body]

    Raises:
        HTTPException: ["Oops! Unexpected mongodb error occurred" or
                        "channel Not Found"]

    Returns:
        channel [dict]: [created channel is returned]
    """
    try:
        response = create_channel(user_id, channel)
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post("/channels/info/{id}", response_description="update channel")
async def edit_channel(id: str, new_data: Change_channel):
    """
    Endpoint to update info of a channel

    Args:
        id (str): [channel id which is being edited]

    Raises:
        HTTPException: ["Oops! Unexpected mongodb error occurred" or
                        "channel Not Found"]

    Returns:
        Channel [dict]: [updated channel info]
    """
    try:
        response = update_channel(id, new_data)
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post("/channels/join/{id}")
async def add_user_to_channel(id: str, user_data: dict):
    """
    Endpoint to add user to a channel

    Args:
        id (str): [channel_id]
        user_data (dict): [user_id[str]: [user being added],
                            req_user[str]: [user sending req(may or may not be admin)]]

    Raises:
        HTTPException: ["Oops! Unexpected mongodb error occurred" or
                        "channel Not Found" or
                        "User Already Exists" or
                        "request denied, user doesn't have permission for this request"
                        "channel type is undefined"]

    Returns:
        membership[dict]: [membership of user is returned]
    """
    try:
        response = join_user(id, user_data)
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.post("/channels/leave/{id}")
async def leave_channel(id: str, user_data: dict):
    """
    Endpoint to for an user to leave a channel

    Args:
        id (str): [channel_id]
        user_data (dict): [user_id[str]: [user being added],
                            req_user[str]: [user sending req(may or may not be admin)]]
    Raises:
        HTTPException: ["Oops! Unexpected mongodb error occurred" or
                        "channel Not Found" or
                        "User Not Found" or
                        "user not in channel"]

    Returns:
        [type]: [description]
    """
    try:
        response = user_leave(id, user_data)
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


@channels_router.delete("/channels/delete/{id}", response_description="Delete channel")
async def delete_channel(id: str, user_data: dict):
    """
    Endpoint to delete a channel

    Args:
        id[str]: [channel_id]
        user_data[dict]: [user_id[str]: [user being added],
                            req_user[str]: [user sending req(may or may not be owner)]]
    Raises:
        HTTPException: ["Oops! Unexpected mongodb error occurred", or
                        "channel Not Found" or
                        "request denied, user doesn't have permission for this request"]

    Returns:
        deleted_channel[dict]: [details of channel deleted(may be useful if we are gonna meke an undo functionality)]
    """
    try:
        response = remove_channel(id, user_data["user_id"])
        return response
    except returnExceptions as err:
        raise HTTPException(
            status_code=Code.error_enum_http[err.error_code], detail=str(err)
        )


# @channels_router.post('/channels/admin/{id}/{user_id}')
# async def make_admin( id: str, user_id: str, user_data: dict):
#     try:
#         response = add_admin(id, user_id, user_data)
#         return response
#     except returnExceptions as err:
#         raise HTTPException(status_code=Code.error_enum_http[err.error_code], detail=str(err))