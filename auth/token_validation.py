
from time import time
import jwt
from config.settings import get_settings
from models.token import TokenData


def decode_access_token(token: str):
    """
    Validates an access token. If the token is valid, it returns the token payload.
    """
    settings = get_settings()
    decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    if decoded_token["expires"] >= int(round(time())):
        return TokenData(user_id=decoded_token["user_id"], profile=decoded_token["profile"]) 
    else:
        return None

