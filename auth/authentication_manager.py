
from datetime import datetime, timedelta, timezone
import logging
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
#from jose import jwt
from passlib.context import CryptContext
from db.firestore_db import FirestoreClient
from config.settings import Settings


class AuthenticationManager():  
    
    def __init__(self, role: str):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        logging.getLogger('passlib').setLevel(logging.ERROR)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
        self.db_client = FirestoreClient(role)        
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def authenticate_user(self, username: str, password: str):
        user = self.db_client.search(username)
        if not user:
            return False
        if not self.verify_password(password, user["password"]):
            return False
        return user
    
    def create_user(self, user: dict):
        account = { 
            'id': user.get("username"),
            'password': self.get_password_hash(user.get("password"))
        }
        self.db_client.create(account)
    
    def create_access_token(self, data: dict, settings: Settings):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
        
