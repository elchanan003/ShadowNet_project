from pydantic import BaseModel, Field


class Agent(BaseModel):
    name               : str = Field(max_length=50)
    specialty          : str = Field(max_length=50)
    is_active          : bool
    completed_missions : int 
    failed_missions    : int  
    agent_rank         : str 

class Mission(BaseModel):
    title             : str = Field(max_length=255)
    description       : str
    location          : str = Field(max_length=255)
    difficulty        : int 
    importance        : int 
    status            : str = Field(max_length=50)
    assigned_agent_id : int | None




