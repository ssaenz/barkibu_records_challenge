import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Config(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    # AWS Configuration
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_s3_bucket_name: str = os.getenv("AWS_S3_BUCKET_NAME", "barkibu-medical-records")
    aws_s3_region: str = os.getenv("AWS_S3_REGION", "us-east-1")

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    environment: str = os.getenv("ENVIRONMENT", "development")


config = Config()
