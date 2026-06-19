from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(_vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    is_vote_exits = db.query(models.Vote).filter(models.Vote.note_id == _vote.v).first()

    if not is_vote_exits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {_vote.note_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.note_id == _vote.note_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if _vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already votes on post")
        
        new_vote = models.Vote(note_id = _vote.note_id, user_id = current_user.id)
        
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote."}
    
    else:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Succesfully deleted vote."}