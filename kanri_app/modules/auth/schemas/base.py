from pydantic import BaseModel
from typing import Union


SECRET_KEY = "7121e7873f381c74a424391580a6675819b11dc00b783be71e4e799b8f1cc637"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: Union[str, None] = None