from fastapi import APIRouter, HTTPException, status, Depends
from .. import database, schemas, models
from .. import hashing
from .. import oauth2
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'])


@router.post("/login/", response_model=schemas.Token)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")

    if not hashing.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

