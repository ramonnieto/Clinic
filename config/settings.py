from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    secret_key: str = "aaaa"
    access_token_expire_minutes: int = 5
    algorithm: str = "AAAA"
    
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()