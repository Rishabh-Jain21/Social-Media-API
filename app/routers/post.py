from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status, HTTPException, APIRouter

from ..database import get_db
from .. import oauth2, db_models
from ..schemas import post_schema
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[post_schema.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(db_models.Post, func.count(db_models.Vote.post_id).label('votes')).join(
        db_models.Vote, db_models.Vote.post_id == db_models.Post.id, isouter=True).group_by(db_models.Post.id).filter(
        db_models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}",  response_model=post_schema.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post = db.query(db_models.Post, func.count(db_models.Vote.post_id).label('votes')).join(
        db_models.Vote, db_models.Vote.post_id == db_models.Post.id, isouter=True).group_by(db_models.Post.id).filter(db_models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schema.PostResponse)
async def create_post(post: post_schema.PostCreate, current_user=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    new_post = db_models.Post(owner_id=current_user.id, ** post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    retrieved_post_query = db.query(
        db_models.Post).filter(db_models.Post.id == id)
    retrieved_post = retrieved_post_query.first()
    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exists")

    if retrieved_post.owner_id == current_user.id:
        retrieved_post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform delete action")


@router.put("/{id}", response_model=post_schema.PostResponse)
async def update_post(id: int, post: post_schema.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    update_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    updated_post = update_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exists")

    if updated_post.owner_id == current_user.id:
        update_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return update_query.first()

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform update action")
