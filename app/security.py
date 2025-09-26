from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.schemas.token import TokenData
from app.schemas.user import User
from jwt.exceptions import InvalidTokenError
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_from_config(username: str):
    """Retrieves user data from your configuration/mock DB."""
    if username == settings.USER_USERNAME:
        # NOTE: In a real app, you would fetch the full user object, 
        # including things like role or disabled status.
        return User(
            username=settings.USER_USERNAME, 
            email="kharazian@example.com", 
            full_name="Amir Kharazian",
            disabled=False
        )
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise InvalidTokenError
    token_data = TokenData(username=username)
    user = get_user_from_config(username=token_data.username) 
    return user
