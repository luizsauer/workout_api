#workout_api\configs\settings.py
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = Field(default='postgresql+asyncpg://workout:workout@localhost/workout')
    # database_url: str = Field(..., env="DATABASE_URL")
    # secret_key: str = Field(..., env="SECRET_KEY")
    # algorithm: str = Field(..., env="ALGORITHM")
    # access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
settings = Settings()
