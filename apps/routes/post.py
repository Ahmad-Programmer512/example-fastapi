from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from ..database import engine, SessionLocal, get_db
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), 
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).all()

    return results


@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post_Create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        new_post = models.Post(owner_id=current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} was not found")

    p, v = post

    return {
        "Post": p,
        "vote": v
    }

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists")
    
    if post.owner_id != current_user.id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform request")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, post: schemas.Post_Create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    posts = db.query(models.Post).filter(models.Post.id == id)
    query_post = posts.first()

    if query_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exists")
    
    if query_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not Authorized to perform request"
        )
    
    posts.update(post.dict(), synchronize_session=False)
    db.commit()


    return {'data': posts.first()}
    