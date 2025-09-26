
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.security import verify_password, create_access_token
from jwt.exceptions import InvalidTokenError
from app.config import settings
from app.security import get_user

from app.schemas.token import Token
from app.schemas.user import User

async def authenticate_user(form_data: OAuth2PasswordRequestForm) -> Token:
    if form_data.username != settings.USER_USERNAME or not verify_password(form_data.password, settings.USER_PASSWORD_HASH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": settings.USER_USERNAME})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(user: User = Depends(get_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user