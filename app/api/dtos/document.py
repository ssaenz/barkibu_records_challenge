from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.domain.models.document import Document


class DocumentUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    document_id: str = Field(..., description="Unique document ID")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type (pdf, jpg, docx, txt, etc.)")
    file_size: int = Field(..., description="File size in bytes")
    created_at: datetime = Field(..., description="Creation timestamp")

    @staticmethod
    def from_domain(document: Document) -> "DocumentUploadResponse":
        return DocumentUploadResponse(
            document_id=document.id,
            filename=document.filename,
            file_type=document.file_type,
            file_size=document.file_size,
            created_at=document.created_at,
        )
