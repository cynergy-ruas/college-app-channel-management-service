from typing import  Optional
from pydantic import BaseModel, Field


class Change_channel(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None 
    type: Optional[str] = None
    category: Optional[str] = None
