
import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jwt import (
    ExpiredSignatureError, 
    ImmatureSignatureError, 
    InvalidAlgorithmError,
    InvalidAudienceError, 
    InvalidKeyError, 
    InvalidSignatureError, 
    InvalidTokenError,
    MissingRequiredClaimError)
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from starlette import status

from auth import auth
from auth.token_validation import decode_access_token


app = FastAPI(debug=True)

class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        unprotected_paths = re.search(r"\/(index|sign-up|login|auth|static)", request.url.path)
        if unprotected_paths is not None:
            return await call_next(request)
        
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token"
                }
            )
        
        try:
            auth_token = bearer_token.split(' ')[1].strip()
            token_payload = decode_access_token(auth_token)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": str(error),
                    "body": str(error)
                },
            )
        else:
            request.state.user_id = token_payload.user_id
            request.state.profile = token_payload.profile
        
        return await call_next(request)  
            
    
app.add_middleware(AuthorizeRequestMiddleware)

app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
     

@app.get("/info")
async def info(request: Request):
    return {"message": "Hi, world!"}


@app.get("/update_patient_data", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="update_patient_data.html", 
        context={})
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, port=6580)