from fastapi import APIRouter, HTTPException
from database.schems import Agent
from database.agent_db import db_agent
import mysql.connector


agent_router = APIRouter(prefix='/agents', tags=['Agents'])


@agent_router.post(path='/', status_code=201)
def add_agent_route(data:Agent):
    if data.agent_rank not in ('Junior', 'Senior', 'Commander'):
        raise HTTPException(status_code=400, detail='Invalit rank')
    
    try:
        agent = db_agent.create_agent(data)
        return {'message': agent}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.get('/')
def all_agents_routes():
    try:
        agents = db_agent.get_all_agents()
        return {'message':agents} 
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')


@agent_router.get('/{id}')
def agent_by_id_route(id:int):
    try:
        agent = db_agent.get_agent_by_id(id)
        if agent is None:
            raise HTTPException(status_code=404, detail='Not Found')
        return {'message': agent}
    
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.put('/{id}')
def update_agent_routes(id:int, data:Agent):
    try:
        status = db_agent.update_agent(id, data)
        if status is None:
            raise HTTPException(status_code=404, detail='Not Found')
        else:
            return {'message': status}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.put('/{id}/deactivate')
def agent_deactivate(id:int):
    try:
        status = db_agent.deactivate_agent(id)
        if status is None:
            raise HTTPException(status_code=404, detail='Not Found')
        else:
            return {'message': 'is_active = False'}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.get('/{id}/performance')
def agent_performance(id:int):
    try:
        status = db_agent.get_agent_performance(id)
        if status is None:
            raise HTTPException(status_code=404, detail='Not Found')
        else:
            return {'message': status}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    