from fastapi import Depends
from app.domain.document_service import DocumentService
from app.domain.document_repository import DocumentRepository
from app.domain.ocr_service import OCRService
from app.adapters.postgres.sql_repository import SQLDocumentRepository
from app.adapters.ocr.tesseract_ocr_adapter import TesseractOCRAdapter
from app.adapters.postgres.database import SessionLocal


def get_document_repository() -> DocumentRepository:
    db = SessionLocal()
    return SQLDocumentRepository(db)


def get_ocr_service() -> OCRService:
    return TesseractOCRAdapter()


def get_document_service(
    repository: DocumentRepository = Depends(get_document_repository),
    ocr_service: OCRService = Depends(get_ocr_service),
) -> DocumentService:
    return DocumentService(repository, ocr_service)
