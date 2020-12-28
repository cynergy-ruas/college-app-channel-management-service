from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel, Field

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

class Membership(BaseModel):
    """
    schema of MEMBERSHIP_DB

    Args:
        BaseModel:  a base class for building model objects/ schemas
    """
    id: Optional[PyObjectId] = Field(alias='_id')
    channel_id: Optional[List[str]] = []

    class Config:
         """
         Convertion of Object ID into String 
         """
         arbitrary_types_allowed = True
         json_encoders = {
             ObjectId: str
             }