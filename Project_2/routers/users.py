from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database, schemas, hashing

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/")
def create_user(user: schemas.UserSchema, db: Session = Depends(database.get_db)):
    user.password = hashing.hash(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user