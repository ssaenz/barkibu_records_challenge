from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any
from app.domain.models.document import Document
from app.adapters.postgres.schema.DocumentSchema import serialize_dataclass


class DocumentUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    document_id: str = Field(..., description="Unique document ID")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type (pdf, jpg, docx, txt, etc.)")
    file_size: int = Field(..., description="File size in bytes")
    extracted_text: Optional[str] = Field(
        None, description="Text extracted from document"
    )
    medical_record: Optional[dict[str, Any]] = Field(
        None, description="Structured medical record data extracted from document"
    )
    created_at: datetime = Field(..., description="Creation timestamp")

    @staticmethod
    def from_domain(document: Document) -> "DocumentUploadResponse":
        return DocumentUploadResponse(
            document_id=document.id,
            filename=document.filename,
            file_type=document.file_type,
            file_size=document.file_size,
            extracted_text=document.extracted_text,
            medical_record=(
                serialize_dataclass(document.medical_record)
                if document.medical_record
                else None
            ),
            created_at=document.created_at,
        )
