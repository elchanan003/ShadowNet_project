from fastapi import APIRouter, HTTPException
from database.schems import Mission
from database.mission_db import MissionDB, db_mission
import mysql.connector


mission_router = APIRouter(prefix='/missions', tags=['Missions'])


@mission_router.post(status_code=201, path='/')
def add_mission_route(data:Mission):
    return db_mission.create_mission(data)

@mission_router.get('/')
def all_missions():
    try:
        return db_mission.get_all_missions()
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
@mission_router.get('/{id}')
def mission_by_id_route(id:int):
    try:
        return db_mission.get_mission_by_id(id)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
@mission_router.put('/missions/{id}/assign/{agent_id}')
def assign_mission_route(id:int, agent_id:int):
    try:
        return db_mission.assign_mission(id, agent_id)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
@mission_router.put('/missions/{id}/start')
def start_mission(id:int):
    try:
        return db_mission.update_mission_status(id, 'IN_PROGRESS')
    except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail='Something went wrong')
        
@mission_router.put('/missions/{id}/complete')
def start_mission(id:int):
    try:
        return db_mission.update_mission_status(id, 'COMPLETED')
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
        
@mission_router.put('/missions/{id}/fail')
def start_mission(id:int):
    try:
        return db_mission.update_mission_status(id, 'FAILED')
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
        
@mission_router.put('/missions/{id}/cancel')
def start_mission(id:int):
    try:
        return db_mission.update_mission_status(id, 'CANCELLED')
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
