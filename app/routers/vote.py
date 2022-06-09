from .. import db_models,  oauth2
from ..schemas import vote_schema
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import database

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: vote_schema.Vote, db: Session = Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):

    post = db.query(db_models.Post).filter(
        db_models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    vote_query = db.query(db_models.Vote).filter(
        db_models.Vote.post_id == vote.post_id, db_models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        new_vote = db_models.Vote(
            post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:

        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exists")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully Deleted Vote"}
