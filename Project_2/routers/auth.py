from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, models, schemas, hashing, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()


    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")
    
    if hashing.verify(user_data.password, user.password) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")
    
    access_token =  oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}