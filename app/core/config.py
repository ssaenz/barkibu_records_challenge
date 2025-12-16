import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Config(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    database_url: str
    environment: str = "development"


config = Config()
