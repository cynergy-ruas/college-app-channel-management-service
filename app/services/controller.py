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
        raise  returnExceptions(1004)   

# def find_channel(id):
#     try:
#         channel_details = channel_DB().find_one({"_id": ObjectId(id)})
        
def fetch_channel(id) -> dict:
    """
    Function to fetch details of a channel with the given id

    Args:
        id (str): id created by the mongoDB

    Returns:
        channel_details[dict]: [the details of the channel requested]
    """
    
    try:
        channel_details = channel_DB().find_one({"_id": ObjectId(id)})
        if channel_details is None:
            raise returnExceptions(1003)
        else:
            channel_details = dict(channel_details)
            channel_details.pop("_id")
            return channel_details
    except pymongo.errors.PyMongoError as err:
        raise  returnExceptions(1004)
        
        

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
        newChannel = channel_DB().insert_one(channel.dict(by_alias=True))
        channel.id = newChannel.inserted_id
        return {'channel': channel}
    except pymongo.errors.PyMongoError as err:
        raise  returnExceptions(1004)
               

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
        check_channel = channel_DB().find_one({"_id": ObjectId(id)})

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

            updated_channel = channel_DB().update_one({"_id": ObjectId(id)}, {"$set": UPDATE_data})
            return "channel info updated"
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)


def remove_channel(id: str, user_id: str) -> dict:
    """
    Args:
    id -> string

    deletes a channel from the database

    return type: string
    """
    try:
        check_owner = channel_DB().find_one({"_id": ObjectId(id)})
        if check_owner is None:
            raise returnExceptions(1003)
        if check_owner['owner']==user_id:
            raise returnExceptions(1005)
        else:    
            delChannel=channel_DB().delete_one({"_id":ObjectId(id)})
            if delChannel.deleted_count>0:
                check_owner.pop("_id")
                return {"channel sucessfully deleted": check_owner}
    except pymongo.errors.PyMongoError as err:
        raise  returnExceptions(1004)
      
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
        check_channel = channel_DB().find_one({"_id": ObjectId(id)})
        
        if check_channel is None:
            raise returnExceptions(1003)
        check_user = membership_DB().find_one({"_id": ObjectId(user_data["user_id"])}) 
        if check_channel['type']== "public":
            if check_user is None: 
                membership = Membership(channel_id=[id])
                new_user = insert_user(user_data["user_id"],membership)
                return {'user joined': new_user}
            else:
                for channel in check_user["channel_id"]:
                    if(channel==id):
                        raise returnExceptions(1006)
                check_user['channel_id'].append(id)
                check_user.pop('_id')
                updated_membership = membership_DB().update_one({"_id": ObjectId(user_data["user_id"])}, {"$set": check_user})
            
            return("user added")        
        
        elif check_channel['type']== "private":
            admins = check_channel['admins']
            for user in admins:
                if(user_data["req_user"]== user):
                    if check_user is None: 
                        membership = Membership(channel_id=[id])
                        new_user = insert_user(user_data["user_id"],membership)
                        return {'user joined': new_user}
                    for channel in check_user["channel_id"]:
                        if(channel==id):
                            raise returnExceptions(1006)
                    check_user['channel_id'].append(id)
                    check_user.pop('_id')                      
                    updated_membership = membership_DB().update_one({"_id": ObjectId(user_data["user_id"])}, {"$set": check_user})
                else:
                    raise returnExceptions(1005)
            return("user added")
        
        else: 
            raise returnExceptions(1009)
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)

def insert_user(user_id: str ,membership : Membership) -> dict:
    """
    function to insert a membership of user into db

    Args:
        membership (Membership): [description]

    Returns:
        membership[dict]: [dict of type Membership from app.database.membership_modal]
    """
    try:
        membership.id = ObjectId(user_id)
        newuser = membership_DB().insert_one(membership.dict(by_alias=True))
        membership.id = newuser.inserted_id
        return membership
    except pymongo.errors.PyMongoError as err:
        raise returnExceptions(1004)

def fetch_user_membership(user_id: str):
    """
    Args:
    id -> string

    displays all channel_ids from the membership database of that particular user_id

    return type: string
    """
    try:          
        check_user = membership_DB().find_one({"_id": ObjectId(user_id)})
        
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
        check_channel = channel_DB().find_one({"_id": ObjectId(id)})
        check_user = membership_DB().find_one({"_id":ObjectId(user_data["user_id"])})

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
                update_membership = membership_DB().update_one({"_id":ObjectId(user_data["user_id"])}, {"$set": check_user})
                updated_membership=membership_DB().find_one({"_id":ObjectId(user_data["user_id"])})
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