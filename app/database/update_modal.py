from typing import  Optional
from pydantic import BaseModel, Field


class Change_channel(BaseModel):

    name: Optional[str]
    description: Optional[str] 
    type: Optional[str] = None
    category: Optional[str] = None
