from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/", response_model=List[schemas.NoteResponse])
def get_Notes(db: Session = Depends(database.get_db),user_id: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    notes = db.query(models.Note).filter(models.Note.title.contains(search)).limit(limit).offset(skip).all()

    return notes

@router.post("/", response_model=schemas.NoteResponse)
def create_Notes(note: schemas.NoteSchema, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    create_note = models.Note(owner_id = current_user.id,**note.dict())

    db.add(create_note)
    db.commit()
    db.refresh(create_note)

    return create_note

@router.put("/{id}", response_model=schemas.NoteResponse)
def update_Note(id: int, note: schemas.NoteSchema, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    notes = db.query(models.Note).filter(models.Note.id == id)
    query_notes = notes.first()

    if query_notes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists")
    
    if query_notes.owner_id != current_user.id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform request")
    
    notes.update(note.dict(), synchronize_session=False)
    db.commit()

    return notes.first()

@router.delete("/{id}", response_model=schemas.NoteResponse)
def delete_Note(id: str, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_note = db.query(models.Note).filter(models.Note.id == id)

    note = query_note.first()

    if note.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id: {id} does not exists")
    
    if note.owner_id != current_user.id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform request")
     
    note.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)