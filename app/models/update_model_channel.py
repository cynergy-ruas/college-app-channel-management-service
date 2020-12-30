from typing import Optional
from pydantic import BaseModel, Field


class Change_channel(BaseModel):
    """
    schema for updating channel to avoid admin or owner updating and created at

    Args:
        BaseModel: a base class for building model objects/ schemas
    """

    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
