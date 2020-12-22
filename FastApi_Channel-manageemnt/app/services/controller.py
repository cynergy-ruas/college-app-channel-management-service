from app.config.config import channel_DB, membership_DB
from app.services.errorCustom import RuasAppExceptions
from fastapi import FastAPI,APIRouter,HTTPException
from app.database.update_modal import Change_channel
from app.database.membership_modal import Membership
from app.database.schema import Channel
from bson.objectid import ObjectId
import datetime
import pymongo

channelsRouter = APIRouter() 

def fetch_channels() -> list:
    """
    Args : none

    Fetching all the channels from the database

    Return type : List
    """
    try:
        channels_list = []
        query = channel_DB().find({"type":"public"})
        for each_channel in query:
            channels_list.append(Channel(**each_channel))
        if not channels_list:
            raise RuasAppExceptions(1008)
        else :
            return channels_list
    except RuasAppExceptions as Error:
        return Error

def fetch_channel(id) -> dict:
    """
    fetch details of a channel with the given _id

    Args:
        id (str): id created by the mongoDB

    Returns:
        channel_details[dict]: [the details of the channel requested]
    """
    try:
        channel_details = channel_DB().find_one({"_id": ObjectId(id)})
        if  channel_details is None:
            raise RuasAppExceptions(1003)
        else:
            channel_details.pop("_id")
            return channel_details
    except RuasAppExceptions as Error:
        return Error

def create_channel(user_id: str, channel: Channel) -> Channel:
    """
    Args : channel -> Channel

    creates new channel in the database

    return type : list

    """
    try:
        if hasattr(channel, 'id'):
            delattr(channel, 'id')
        # user_details = dict(membership_DB().find_one({"user_id": user_id}))
        # print(user_details)
        # if  user_details is None:
        #     raise RuasAppExcptions(1003)
        channel.owner = user_id
        channel.admins.append(user_id)
        channel.created_at= datetime.datetime.now()
        if(channel.description==""):
            channel.description = channel.name
        try:
            newChannel = channel_DB().insert_one(channel.dict(by_alias=True))
            channel.id = newChannel.inserted_id
            return {'channel': channel}
        except pymongo.errors.PyMongoError as err:
            raise  RuasAppExceptions(1004)
    except RuasAppExceptions as err:
        return err
               
def update_channel(id: str, new_data: Change_channel) -> Channel:
    try:
        check_channel = channel_DB().find_one({"_id": ObjectId(id)})
        if check_channel is None:
            raise  RuasAppExceptions(1003)
        else:
            UPDATE_data = dict(new_data) 

            if(UPDATE_data['name']== None):
                UPDATE_data['name']= check_channel['name']

            if(UPDATE_data['description']== None):
                UPDATE_data['description']= check_channel['description']

            if(UPDATE_data['type']== None):
                UPDATE_data['type']= check_channel['type']

            if(UPDATE_data['category']== None):
                UPDATE_data['category']= check_channel['category']

        #need to add a checking logic if the channel exist or not using above request
            updated_channel = channel_DB().update_one({"_id": ObjectId(id)}, {"$set": UPDATE_data})
            return "channel is updated"

    except RuasAppExceptions as err:
        return err

def remove_channel(id: str, user_id: str):
    """
    Args:
    id -> string

    deletes a channel from the database

    return type: string
    """
    try:
          
        check_owner = channel_DB().find_one({"_id": ObjectId(id)})
        if check_owner is None:
            raise RuasAppExceptions(1009)

        else:
            if(check_owner['owner']==user_id):
                check_owner.pop("_id")
                delChannel=channel_DB().delete_one({"_id":ObjectId(id)})
                if delChannel.deleted_count>0:
                    return {"channel sucessfully deleted": check_owner}
            else:
                return {'request denied' : "user does not have permission to delete channel"}
    except RuasAppExceptions as Error:
        return Error

# user_data = {"user_id": "[user who need to be added]", "req_user": "[user who is requesting this service]"}        
def join_user(id: str, user_data: dict):    
    try:
        check_channel = channel_DB().find_one({"_id": ObjectId(id)})
        if check_channel is None:
            # return "channel not found, wrong id"
            raise RuasAppExceptions(1003) 
        if(check_channel['type']== "public"):
            check_user = membership_DB().find_one({"user_id":user_data["user_id"]})
            if check_user is None:
                # membership: Membership 
                membership = Membership(user_id= user_data["user_id"], channel_id=[id])
                
                new_user = insert_user(membership)
                return {'user joined': new_user}
            else:
                raise RuasAppExceptions(1001)
            #return 1
    # user = {"user_id":user_data["user_id"], "channel_id":[id]}
    # if hasattr(user, 'id'):
    #      delattr(user, 'id')
    # new_user = membership_DB().insert_one(user)
    # user.id = new_user.inserted_id
    # return {'user joined': user}    
    except RuasAppExceptions as Error:
        return Error

def insert_user(membership : Membership):
    print(membership)
    if hasattr(membership, 'id'):
        delattr(membership, 'id')
    newuser = membership_DB().insert_one(membership.dict(by_alias=True))
    # membership.id = newuser.inserted_id
    return membership
