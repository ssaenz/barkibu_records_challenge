import uuid
from app.domain.models.document import Document
from app.domain.repositories.document_repository import DocumentRepository
from app.domain.repositories.file_repository import FileRepository


class DocumentService:
    def __init__(self, repository: DocumentRepository, storage: FileRepository):
        self.repository = repository
        self.storage = storage

    def create_document(
        self, filename: str, file_type: str, file_data: bytes, 
    ) -> Document:
        """
        Create and store a document
        
        Business logic:
        - Generate unique ID
        - Generate file path
        - Store file in storage
        - Create document record
        
        Args:
            filename: Original filename
            file_type: File extension (pdf, jpg, etc.)
            file_data: File content as bytes
            
        Returns:
            Created Document domain object
        """
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Generate file path (business logic for organizing files)
        file_path = f"documents/{document_id}/{filename}"
        
        # Store file in storage adapter
        self.storage.upload(file_data, file_path)
        
        # Create domain model
        document = Document(
            id=document_id,
            filename=filename,
            file_type=file_type,
            file_size=len(file_data),
            path=file_path,
        )
        
        # Persist using repository
        saved_document = self.repository.save(document)
        
        return saved_document

        # Persist using repository
        saved_document = self.repository.save(document)
        
        return saved_document
        return self.repository.delete(document_id)
