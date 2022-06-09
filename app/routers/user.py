
from .. import oauth2
from .. import db_models, utils
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import user_schema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


"""
Get Information for a user with a id
"""


@router.get("/{id}",  response_model=user_schema.UsersOut)
async def get_user(id: int, db: Session = Depends(get_db)) -> None:
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exists")
    return user


"""
Create User
"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UsersOut)
async def create_user(user: user_schema.UsersCreate, db: Session = Depends(get_db)) -> None:

    check_if_user_already_exists_query = db.query(db_models.User).filter(
        db_models.User.email == user.email)

    if check_if_user_already_exists_query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    # hash the paswword of the user
    user.password = utils.hash(user.password)
    new_user = db_models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
