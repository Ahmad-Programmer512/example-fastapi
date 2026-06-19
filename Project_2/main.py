from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from . import database, models
from .routers import notes, users, auth, vote

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)