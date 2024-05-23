import logging
from passlib.context import CryptContext
from db.firestore_db import FirestoreClient


class AuthenticationManager():  
    
    def __init__(self, role: str):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        logging.getLogger('passlib').setLevel(logging.ERROR)
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

