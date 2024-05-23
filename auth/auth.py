from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from auth.authentication_manager import AuthenticationManager
from models.token import Token
from config.settings import Settings, get_settings


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

   
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    profile: Annotated[str, Form()]
):
    user = {'username': username, 'password': password}
    auth_manager = AuthenticationManager(profile)
    auth_manager.create_user(user)
    
@router.post("/token")
async def login_for_access_token(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    profile: Annotated[str, Form()],
    settings: Annotated[Settings, Depends(get_settings)]
) -> Token:
    auth_manager = AuthenticationManager(profile)    
    user = auth_manager.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_manager.create_access_token(data={"sub": user.username}, settings=settings)
    return Token(access_token=access_token, token_type="bearer")
