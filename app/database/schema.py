from bson import ObjectId
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo import MongoClient
from app.config.config import channel_DB


class PyObjectId(ObjectId):
    """
    To use with an already created database, we’re going to create a custom validator class. 

    To create a model in Pydantic library,
    you have to declare a class that inherits from the BaseModel class. 
    All the fields you want to validate and 
    make part of the model must be declared as attributes.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

#Basically, we have implemented  two methods, get_validators and validate, so Pydantic knows how to deal with it.
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

#creating channel class to store schema 
class Channel(BaseModel):
    """
     The Schema for our data model 
    
     Schema :
        _id -> Object ID,
        Name -> string,
        description -> string,
        members -> List[string]
        type -> string
        dp -> string
        admins -> List[string]
    """
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    description: Optional[str] = None
    members: List[str] = []
    type: str
    dp:Optional[str]
    admins:List[str] = []

    class Config:
        """
        Convertion of Object ID into String 
        """
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
            }