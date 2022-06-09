from pydantic import BaseModel
from pydantic.typing import Literal


class Vote(BaseModel):
    """
    post_id: post you want to vote on
    dir: 1 means vote the post if vote does not exists, 0 means remove vote if vote exists
    """
    post_id: int
    dir: int = Literal[0, 1]
