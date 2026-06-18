from fastapi import APIRouter, HTTPException
from database.schems import Agent
from database.agent_db import db_agent
import mysql.connector


agent_router = APIRouter(prefix='/agents', tags=['Agents'])


@agent_router.post(path='/', status_code=201)
def add_agent_route(data:Agent):
    try:
        agent = db_agent.create_agent(data)
        return agent 
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.get('/')
def all_agents_routes():
    try:
        agents = db_agent.get_all_agents()
        return agents 
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
   
    
@agent_router.get('/{id}')
def agent_by_id_route(id:int):
    try:
        agent = db_agent.get_agent_by_id(id)
        return agent
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.put('/{id}')
def update_agent_routes(id:int, data:Agent):
    try:
        return db_agent.update_agent(id, data)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.put('/{id}/deactivate')
def agent_deactivate(id:int):
    try:
        return db_agent.deactivate_agent(id)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    

@agent_router.get('/{id}/performance')
def agent_performance(id:int):
    try:
        return db_agent.get_agent_performance(id)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    