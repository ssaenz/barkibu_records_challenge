from functools import lru_cache
from fastapi import Depends
from app.domain.document_service import DocumentService
from app.domain.document_repository import DocumentRepository
from app.domain.text_extractor import TextExtractor
from app.domain.medical_record_extractor import MedicalRecordExtractor
from app.adapters.postgres.sql_repository import SQLDocumentRepository
from app.adapters.ocr.tesseract_ocr_adapter import TesseractOCRAdapter
from app.adapters.spacy.spacy_medical_record_extractor import (
    SpacyMedicalRecordExtractor,
)
from app.adapters.postgres.database import SessionLocal
from app.core.config import config


def get_document_repository() -> DocumentRepository:
    db = SessionLocal()
    return SQLDocumentRepository(db)


def get_text_extractor() -> TextExtractor:
    return TesseractOCRAdapter()


@lru_cache()
def get_medical_record_extractor() -> MedicalRecordExtractor:
    return SpacyMedicalRecordExtractor(model_name=config.spacy_model)


def get_document_service(
    repository: DocumentRepository = Depends(get_document_repository),
    text_extractor: TextExtractor = Depends(get_text_extractor),
    medical_record_extractor: MedicalRecordExtractor = Depends(
        get_medical_record_extractor
    ),
) -> DocumentService:
    return DocumentService(repository, text_extractor, medical_record_extractor)
