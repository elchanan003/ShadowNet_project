from fastapi import FastAPI
from database.db_connection import db
from routes.agent_routes import agent_router
from routes.mission_routes import mission_router
from routes.report_routes import router_report

app = FastAPI()
app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(router_report)


@app.on_event("startup")
async def startup_event():
    db.create_database()
    db.create_tables()