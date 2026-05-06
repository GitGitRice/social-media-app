import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from web_app.crud import get_user_by_id
from web_app.database import get_session
from web_app.models import User, ModelError
import os
from dotenv import load_dotenv

# Load the variables from .env into the system environment
load_dotenv()

# read system environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-for-local-dev") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

# Tell FastAPI on which end point to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def get_password_hash(password: str) -> str:
    """Returns the hash of the provided password."""
    # 1. Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # 3. Return as a string to store in DB
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if plain password matches the hashed password."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict):
    """Returns an access token to ... """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    # PyJWT requires the algorithms list for security
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """gets current user based on user id (not user_name)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # FIX: Get the value first, then check if it's None to satisfy the IDE
        sub_value = payload.get("sub")
        if sub_value is None:
            raise credentials_exception
        
        # sub_value is now guaranteed to be not-None
        user_id: int = int(sub_value) 
    except JWTError:
        raise credentials_exception

    # fetch user by id
    result = get_user_by_id(id=user_id, session=session)
    if isinstance(result, ModelError):
        raise credentials_exception
    
    return result