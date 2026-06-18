from fastapi import APIRouter, HTTPException
from database.schems import Mission
from database.agent_db import db_agent
from database.mission_db import db_mission
import mysql.connector


mission_router = APIRouter(prefix='/missions', tags=['Missions'])


@mission_router.post(status_code=201, path='/')
def add_mission_route(data:Mission):
    if not (0 < data.difficulty < 11):
        raise HTTPException(status_code=400)
    if not (0 < data.importance < 11):
        raise HTTPException(status_code=400)

    try:
        return {'message':db_mission.create_mission(data)}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')


@mission_router.get('/')
def all_missions():
    try:
        return {'message':db_mission.get_all_missions()}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
@mission_router.get('/{id}')
def mission_by_id_route(id:int):
    try:
        status = db_mission.get_mission_by_id(id)
        if status is None:
            raise HTTPException(status_code=404, detail='Not Found')
        else:
            return {'message':status}
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

    mission = db_mission.get_mission_by_id(id)
    if mission and mission['status'] != 'ASSIGNED':
        raise HTTPException(status_code=400)
    
    try:
        status = db_mission.update_mission_status(id, 'IN_PROGRESS')
        if status is None:
            raise HTTPException(status_code=404)
        else:
            return {'message':'IN_PROGRESS'}
    except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail='Something went wrong')


@mission_router.put('/missions/{id}/complete')
def completed_mission(id:int):

    mission = db_mission.get_mission_by_id(id)
    if mission and mission['status'] != 'IN_PROGRESS':
        raise HTTPException(status_code=400)
    
    try:
        status = db_mission.update_mission_status(id, 'COMPLETED')
        if status is None:
            raise HTTPException(status_code=404)
        else:
            db_agent.increment_completed()
            return {'message':'Updated successfully'}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')


@mission_router.put('/missions/{id}/fail')
def failed_mission(id:int):

    mission = db_mission.get_mission_by_id(id)
    if mission and mission['status'] != 'IN_PROGRESS':
        raise HTTPException(status_code=400)
    
    try:
        status = db_mission.update_mission_status(id, 'FAILED')
        if status is None:
            raise HTTPException(status_code=404)
        else:
            db_agent.increment_failed()
            return {'message':'Updated successfully'}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')


@mission_router.put('/missions/{id}/cancel')
def canceled_mission(id:int):
        
    mission = db_mission.get_mission_by_id(id)
    if mission and mission['status'] != 'NEW' or mission['status'] != 'ASSIGNED':
        raise HTTPException(status_code=400)
    
    try:
        status = db_mission.update_mission_status(id, 'CANCELLED')
        if status is None:
            raise HTTPException(status_code=404)
        else:
            return {'message':'Updated successfully'}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
