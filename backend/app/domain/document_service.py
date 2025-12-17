import uuid
import logging
import time
from typing import Optional
from app.domain.models.document import Document
from app.domain.document_repository import DocumentRepository
from app.domain.text_extractor import TextExtractor
from app.domain.medical_record_extractor import MedicalRecordExtractor

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
        self,
        repository: DocumentRepository,
        text_extractor: TextExtractor,
        medical_record_extractor: Optional[MedicalRecordExtractor] = None,
    ):
        self.repository = repository
        self.text_extractor = text_extractor
        self.medical_record_extractor = medical_record_extractor

    def create_document(
        self,
        filename: str,
        file_type: str,
        file_data: bytes,
    ) -> Document:
        document_id = str(uuid.uuid4())

        start_time = time.time()
        logger.info(f"Starting text extraction for document {document_id} ({filename})")
        extracted_text = self.text_extractor.extract_text(file_data, file_type)
        ocr_duration = time.time() - start_time
        logger.info(
            f"Text extraction for document {document_id} took {ocr_duration:.2f} seconds"
        )

        medical_record = None
        if self.medical_record_extractor and extracted_text:
            try:
                start_time = time.time()
                logger.info(
                    f"Starting medical record extraction for document {document_id}"
                )
                medical_record = self.medical_record_extractor.extract(extracted_text)
                extraction_duration = time.time() - start_time
                logger.info(
                    f"Medical record extraction for document {document_id} took {extraction_duration:.2f} seconds"
                )
            except Exception as e:
                logger.error(
                    f"Error extracting medical record for document {document_id}: {e}"
                )
                pass

        document = Document(
            id=document_id,
            filename=filename,
            file_type=file_type,
            file_size=len(file_data),
            file_data=file_data,
            extracted_text=extracted_text,
            medical_record=medical_record,
        )
        saved_document = self.repository.save(document)
        return saved_document
