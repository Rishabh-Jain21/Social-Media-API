from sqlalchemy.orm import Session
from fastapi import Depends,  status, HTTPException, APIRouter
from .. import db_models, utils
from ..database import get_db
from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    {
        "username":some_username
        "password":some_password

        In postman it is passed as a form data parameter
    }

    """
    user = db.query(db_models.User).filter(
        db_models.User.email == user_credentials.username
        and
        db_models.User.password == utils.hash(user_credentials.password)

    ).first()

    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # Create token and return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
