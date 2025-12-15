import boto3
from app.domain.repositories.file_repository import FileRepository
from app.core.config import config


class S3FileRepository(FileRepository):
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            region_name=config.aws_s3_region,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
        )
        self.bucket = config.aws_s3_bucket_name

    def upload(self, file_data: bytes, storage_key: str) -> dict:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=storage_key,
                Body=file_data,
            )
            return {
                "bucket": self.bucket,
                "key": storage_key,
                "size": len(file_data),
                "success": True,
            }
        except Exception as e:
            raise Exception(f"Failed to upload file to S3: {str(e)}")
