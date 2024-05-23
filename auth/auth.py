from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import jwt
from starlette import status
from auth.authentication_manager import AuthenticationManager
from config.settings import get_settings
from models.token import Token


router = APIRouter(tags=['auth'])

templates = Jinja2Templates(directory="templates")
       
def create_access_token(user_id: str, profile: str):
    settings = get_settings()
    to_encode = {"user_id": user_id, "profile": profile}
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"expires": int(round(expire.timestamp()))})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={})
    

@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    profile: Annotated[str, Form()]
) -> Token:
    user = {'username': username, 'password': password}
    auth_manager = AuthenticationManager(profile)
    ## Check if user already exists, and if errors... TODO  
    auth_manager.create_user(user)
    access_token = create_access_token(username, profile)
    return Token(access_token=access_token, token_type="bearer")

    
@router.post("/auth/token")
async def login_for_access_token(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    profile: Annotated[str, Form()]
) -> Token:
    print("I AM HEEEERE")
    auth_manager = AuthenticationManager(profile)    
    user = auth_manager.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user["id"], profile)
    return Token(access_token=access_token, token_type="bearer")
