import uuid
from app.domain.models.document import Document
from app.domain.document_repository import DocumentRepository
from app.domain.text_extractor import TextExtractor


class DocumentService:
    def __init__(self, repository: DocumentRepository, text_extractor: TextExtractor):
        self.repository = repository
        self.text_extractor = text_extractor

    def create_document(
        self,
        filename: str,
        file_type: str,
        file_data: bytes,
    ) -> Document:
        document_id = str(uuid.uuid4())
        extracted_text = self.text_extractor.extract_text(file_data, file_type)
        document = Document(
            id=document_id,
            filename=filename,
            file_type=file_type,
            file_size=len(file_data),
            file_data=file_data,
            extracted_text=extracted_text,
        )
        saved_document = self.repository.save(document)
        return saved_document
