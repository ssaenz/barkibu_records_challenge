from fastapi import Depends
from app.domain.document_service import DocumentService
from app.domain.document_repository import DocumentRepository
from app.domain.text_extractor import TextExtractor
from app.adapters.postgres.sql_repository import SQLDocumentRepository
from app.adapters.ocr.tesseract_ocr_adapter import TesseractOCRAdapter
from app.adapters.postgres.database import SessionLocal


def get_document_repository() -> DocumentRepository:
    db = SessionLocal()
    return SQLDocumentRepository(db)


def get_text_extractor() -> TextExtractor:
    return TesseractOCRAdapter()


def get_document_service(
    repository: DocumentRepository = Depends(get_document_repository),
    text_extractor: TextExtractor = Depends(get_text_extractor),
) -> DocumentService:
    return DocumentService(repository, text_extractor)
