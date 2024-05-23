from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from auth import auth
from config.settings import Settings


app = FastAPI()
app.include_router(auth.router)

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={})
    
    

"""
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    password_manager = PasswordManager()
    print(f"Password Hash: {password_manager.set_password(form_data.password)}")
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    if not password_manager.check_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
"""


@app.get("/update_patient_data", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="update_patient_data.html", 
        context={})
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, port=6580)