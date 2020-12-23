from fastapi import FastAPI,APIRouter,HTTPException
from app.database.schema import Channel
from app.database.update_modal_channel import Change_channel
from app.database.membership_modal import Membership
from bson.objectid import ObjectId
channelsRouter = APIRouter() 
from app.config.config import channel_DB, membership_DB
from bson import ObjectId
import datetime
from app.services.errorCustom import returnExceptions
import pymongo

def find_channel(id: str):
    """Function to find a channel using id

    Args:
        id ([str]): [channel id]

    Raises:
        returnExceptions: ["Oops! Unexpected mongodb error occurred"]

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

    Raises:
        returnExceptions: [Oops! Unexpected mongodb error occurred]

    Returns:
        [type]: [description]
    """

    newChannel = channel_DB().insert_one(channel.dict(by_alias=True))
    return newChannel
    

def update_channelinfo(id: str, UPDATE_data: dict):
    """[summary]

    Args:
        id (str): [description]
        UPDATE_data (dict): [description]

    Returns:
        [type]: [description]
    """
    update_channel = channel_DB().update_one({"_id": ObjectId(id)}, {"$set": UPDATE_data})
    return update_channel
    

def delete_channel(id: str): 
    """[summary]

    Args:
        id (str): [description]

    Returns:
        [type]: [description]
    """
    delChannel=channel_DB().delete_one({"_id":ObjectId(id)})
    return delChannel


def find_membership(user_id: str):
    """[summary]

    Args:
        user_id (str): [description]

    Returns:
        [type]: [description]
    """
    user_details = membership_DB().find_one({"_id":ObjectId(user_id)})
    return user_details


def insert_membership(user_id: str ,id : str) -> dict:
    """
    function to insert a membership of user into db

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
    """[summary]

    Args:
        user_id (str): [description]
        new_data (dict): [description]

    Returns:
        [type]: [description]
    """
    updating_membership = membership_DB().update_one({"_id": ObjectId(user_id)}, {"$set": new_data})
    return updating_membership


def fetch_channels() -> list:
    """
    Function to fetch all channels from the db

    Returns:
        channels[list]: [list of channel[dict]]
    """
    try:
        query = channel_DB().find({"type":"public"})
        if query is None:
            raise returnExceptions(1008)
        channels_list = []
        for each_channel in query:
            channels_list.append(Channel(**each_channel))
        return channels_list
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)

  

def fetch_channel(id) -> dict:
    """
    Function to fetch details of a channel with the given id

    Args:
        id (str): id created by the mongoDB

    Returns:
        channel_details[dict]: [the details of the channel requested]
    """
    
    try:
        channel_details = find_channel(id)
        if channel_details is None:
            raise returnExceptions(1003)
        else:
            channel_details = dict(channel_details)
            channel_details.pop("_id")
            return channel_details
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)
        
        

def create_channel(user_id: str, channel: Channel) -> dict:
    """
    Function to insert a channel into db

    [explanation]

    Raises:
        returnExceptions: [mongo errors]

    Returns:
        [dict]: [created channel is returned]
    """
    try:
        if hasattr(channel, 'id'):
            delattr(channel, 'id')
        channel.owner = user_id
        channel.admins.append(user_id)
        channel.created_at= datetime.datetime.now()
        if(channel.description==""):
            channel.description = channel.name
        newChannel = insert_channel(channel)
        channel.id = newChannel.inserted_id
        check_user = find_membership(user_id)
        if check_user is None:
            insert_membership(user_id, str(channel.id))
        else:
            check_user['channel_id'].append(str(channel.id))
            check_user.pop('_id')
            updated_membership = update_membership(user_id,check_user)
        return {'channel': channel}
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)
               

def update_channel(id: str, new_data: Change_channel) -> dict:
    """
    Function to update info of a channel 

    [explanation]

    Args:
        id (str): [channel_id]
        new_data (Change_channel): [description]

    Returns:
        "channel updated"
    """
    try:
        check_channel = find_channel(id)

        if check_channel is None:
            raise returnExceptions(1003)
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

            updating_channel = update_channelinfo(id, UPDATE_data)
            channel_details = find_channel(id)
            channel_details.pop("_id")
            return {"channel info updated" : channel_details}
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)

def remove_channel(id: str, user_id: str) -> dict:
    """[summary]

    Args:
        id (str): [description]
        user_id (str): [description]

    Raises:
        returnExceptions: [description]
        returnExceptions: [description]
        returnExceptions: [description]

    Returns:
        dict: [description]
    """
    try:
        check_owner = find_channel(id)
        if check_owner is None:
            raise returnExceptions(1003)
        if check_owner['owner']!=user_id:
            print(check_owner['owner'],user_id)
            raise returnExceptions(1005)
        else:    
            delChannel= delete_channel(id)
            if delChannel.deleted_count>0:
                check_owner.pop("_id")
                return {"channel sucessfully deleted": check_owner}
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)  

def join_user(id: str, user_data: dict) -> dict:    
    """
    Function to add channel to membership of user
        or create user in membership

    Args:
        id (str): [channel_id]
        user_data (dict): [user_id[str]: [user being added], 
                            req_user[str]: [user sending req(may or may not be admin)]]

    Raises:
        returnExceptions: ["channel Not Found"]
        returnExceptions: ["User Already Exists"]
        returnExceptions: ["request denied, user doesn't have permission for this request"]

    Returns:
        membership[dict]: [description]
    """
    try:
        check_channel = find_channel(id)
        
        if check_channel is None:
            raise returnExceptions(1003)
        check_user = find_membership(user_data["user_id"]) 
        if check_channel['type']== "public":
            if check_user is None: 
                new_user = insert_membership(user_data["user_id"],id)
                return {'user joined': new_user}
            else:
                for channel in check_user["channel_id"]:
                    if(channel==id):
                        raise returnExceptions(1006)
                check_user['channel_id'].append(id)
                check_user.pop('_id')
                updated_membership = update_membership(user_data["user_id"],check_user)            
            return("user added")        
        
        elif check_channel['type']== "private":
            admins = check_channel['admins']
            for user in admins:
                if(user_data["req_user"]== user):
                    if check_user is None:
                        new_user = insert_membership(user_data["user_id"],id)
                        return {'user joined': new_user}
                    for channel in check_user["channel_id"]:
                        if(channel==id):
                            raise returnExceptions(1006)
                    check_user['channel_id'].append(id)
                    check_user.pop('_id')                      
                    updated_membership = update_membership(user_data["user_id"],check_user)
                else:
                    raise returnExceptions(1005)
            return("user added")
        
        else: 
            raise returnExceptions(1009)
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)



def fetch_user_membership(user_id: str):
    """[summary]

    Args:
        user_id (str): [description]

    Raises:
        returnExceptions: [description]
        returnExceptions: [description]

    Returns:
        [type]: [description]
    """
    try:          
        check_user = find_membership(user_id)
        
        if check_user is None:
            raise returnExceptions(1002)
        else:
            if check_user['_id']==ObjectId(user_id):
                check_user.pop("_id")
                return {"user channels": check_user["channel_id"]}
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)

def user_leave(id: str, user_data: dict)-> list:    

    try:
        check_channel = find_channel(id)
        check_user = find_membership(user_data["user_id"])

        if check_channel is None:
            raise returnExceptions(1003) 
        
        elif check_user is None: 
            raise returnExceptions((1002))
        
        else:
            list_of_channels = check_user['channel_id'] 
            if id not in list_of_channels:
                raise returnExceptions(1007)
            else:
                list_of_channels.remove(id)
                check_user['channel_id'] = list_of_channels 
                updating_membership = update_membership(user_data["user_id"],check_user)
                updated_membership = find_membership(user_data["user_id"])
                updated_membership.pop("_id")
                return {"user channels": updated_membership["channel_id"]}
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)

# V1 
# def add_admin(id:str, user_id: str, user_data: dict):
#     try: 
#        check_channel = channel_DB().find_one({"_id": ObjectId(id)})
#        if check_channel is None:
#            raise returnExceptions() 