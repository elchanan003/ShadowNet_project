from fastapi import FastAPI
from routes.agent_routes import agent_router
from database.db_connection import db


app = FastAPI()
app.include_router(agent_router)


@app.on_event("startup")
async def startup_event():
    db.create_database()
    db.create_tables()