from fastapi import Depends
from app.domain.services.document_service import DocumentService
from app.domain.repositories.document_repository import DocumentRepository
from app.domain.repositories.file_repository import FileRepository
from app.adapters.postgres.sql_repository import SQLDocumentRepository
from app.adapters.s3.s3_adapter import S3FileRepository
from app.adapters.postgres.database import SessionLocal


def get_document_repository() -> DocumentRepository:
    db = SessionLocal()
    return SQLDocumentRepository(db)


def get_file_repository() -> FileRepository:
    return S3FileRepository()


def get_document_service(
    repository: DocumentRepository = Depends(get_document_repository),
    file_repository: FileRepository = Depends(get_file_repository),
) -> DocumentService:
    return DocumentService(repository, file_repository)
