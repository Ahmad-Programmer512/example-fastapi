from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas                          
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
from .. import hashing

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hashing.hash(user.password)
    
    # Use .model_dump() for Pydantic v2, or keep .dict() for v1
    user_data = user.model_dump() 
    user_data["password"] = hashed_password
    
    new_user = models.User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        # Fixed the typo from "ith" to "with"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id: {id} does not exist"
        )
    
    return user
