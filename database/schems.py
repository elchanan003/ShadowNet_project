from pydantic import BaseModel, Field
from typing import Literal


class Agent(BaseModel):
    name               : str = Field(max_length=50)
    specialty          : str = Field(max_length=50)
    is_active          : bool
    completed_missions : int 
    failed_missions    : int  
    agent_rank         : str = Literal['Junior', 'Senior', 'Commander']

class Mission(BaseModel):
    title             : str = Field(max_length=255)
    description       : str
    location          : str = Field(max_length=255)
    difficulty        : int = Field(ge=0, le=10)
    importance        : int = Field(ge=0, le=10)
    status            : str = Field(max_length=50)
    assigned_agent_id : int | None




