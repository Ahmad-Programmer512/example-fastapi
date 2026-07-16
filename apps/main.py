from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import post, user, auth, vote
from . import schemas, models
from .database import engine

# FIXED: Set redirect_slashes to False to kill the 307 redirect loops
app = FastAPI(redirect_slashes=False)

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root(): 
    return {"message": "hello"}

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vote.router)
