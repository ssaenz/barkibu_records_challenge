"""Pytest configuration and fixtures"""
import os
import pytest
from moto import mock_aws
import boto3


@pytest.fixture(scope="session", autouse=True)
def setup_aws_credentials():
    """Set fake AWS credentials for testing"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_S3_REGION"] = "us-east-1"


@pytest.fixture(autouse=True)
def mock_s3_with_bucket():
    """Create mocked S3 with test bucket before each test"""
    with mock_aws():
        # Create S3 client and bucket
        s3_client = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id="testing",
            aws_secret_access_key="testing",
        )
        s3_client.create_bucket(Bucket="barkibu-medical-records")
        yield


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    from app.adapters.postgres.database import engine, Base, SessionLocal

    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    yield
