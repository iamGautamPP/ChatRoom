from pydantic import BaseModel, StringConstraints, EmailStr
from typing import Annotated

class User(BaseModel):
    username : Annotated[str, StringConstraints(max_length=20, min_length=6)]
    email: EmailStr

class UserSignup(User):
    password:Annotated[str, StringConstraints(min_length=8)]

class UserLogin(BaseModel):
    username:str
    password:str

class UserInDB(User):
    hashed_password:str

class Token(BaseModel):
    access_token:str
    token_type:str