from fastapi import APIRouter, HTTPException
from database.mission_db import db_mission
from database.agent_db import db_agent
import mysql.connector


router_report = APIRouter(prefix='/reports', tags=['Reports'])


@router_report.get('/')
def general_system_report():
    try:
        return {'message':{
            "Active_agent_count" : db_agent.count_active_agents(), 
            "total_missions": db_mission.count_all_missions(),
            "open_missions":db_mission.count_open_missions(),
            "compleated_mission":db_mission.count_by_status('COMPLETED'),
            "failed_missions":db_mission.count_by_status('FAILED'),
            "critical_missions":db_mission.count_critical_missions()
        }}
    
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail='somthing wrong')
    

@router_report.get('/missions-by-status')
def mission_by_status_report():
    try:
        return {'message':{
            "open":db_mission.count_open_missions(),
            "in_progress":db_mission.count_open_missions(),
            "completed":db_mission.count_by_status('COMPLETED'),
            "failed":db_mission.count_by_status('FAILED')
        }}
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail='somthing wrong')

@router_report.get('/top-agent')
def top_agent_report():
    try:
        status = db_mission.get_top_agent()
        if status is None:
            raise HTTPException(status_code=404, detail='No top agent')
        else:
            return {"message":status}
        
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail='somthing wrong')