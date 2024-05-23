from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    secret_key: str
    access_token_expire_minutes: int
    algorithm: str
    
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()