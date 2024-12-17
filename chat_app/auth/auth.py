from datetime import timedelta, datetime, UTC
from typing import Annotated
from models.user_model import User, UserSignup
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from utils.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRY_MINUTES
from models.user_model import UserSignup, UserInDB,Token, UserLogin, User
from core.fake_db import DB

db = DB()

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(data:UserSignup):
    if data.username in db.users:
        return {"message":f"user with username {data.username} already exists"}

    user = UserInDB(
        username=data.username,
        email=data.email,
        hashed_password=bcrypt_context.hash(data.password)
    )
    db.add_users(user)

    return {"message":"User has been created Successfully"}

@router.post("/login")
async def login_user(data:UserLogin)->Token:
    username = data.username
    password = data.password

    user = authenticate(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password")
    else:
        token = create_access_token(user.username)
    return Token(access_token=token, token_type="bearer")

def authenticate(username:str, password:str):
    if not db.user_exists(username):
        return False
    hashed_password = db.users[username].get("hashed_password")
    if not bcrypt_context.verify(password, hashed_password):
        return False
    return UserInDB(**db.users[username])

def create_access_token(username:str):
    data = {"sub":username}

    expiry= datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES) #after this minutes the user will have to sign up again
    data.update({"exp":expiry})

    encoded_data = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_data

def verify_jwt(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing User information")
        username = payload['sub']
        user = db.users[username]
        return User(username=user.get("username"), email=user.get("email"))
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
    


    

    

