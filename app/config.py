from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)
    
    database_url: str
    database_url_sync: Optional[str] = None
    debug: bool = False
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"


settings = Settings()

