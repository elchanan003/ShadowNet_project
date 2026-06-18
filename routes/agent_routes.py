from fastapi import APIRouter, HTTPException
from database.schems import Agent
from pydantic import ValidationError
from database.agent_db import AgentDB, db_agent


agent_router = APIRouter(prefix='/agents')


@agent_router.post('/')
def add_agent_route(data:Agent):
    try:
        agent = db_agent.create_agent(data)
        return agent if agent else 'faild'
    except ValidationError:
        raise HTTPException(status_code=400, detail='bad request')
    except Exception as e:
        raise HTTPException(status_code=500, detail='Something went wrong, please try again')