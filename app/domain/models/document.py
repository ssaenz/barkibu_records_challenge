from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.models.medical_record import MedicalRecord


class Document:

    def __init__(
        self,
        id: str,
        filename: str,
        file_type: str,
        file_size: int,
        file_data: bytes,
        extracted_text: Optional[str] = None,
        medical_record: Optional["MedicalRecord"] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.filename = filename
        self.file_type = file_type
        self.file_size = file_size
        self.file_data = file_data
        self.extracted_text = extracted_text
        self.medical_record = medical_record
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"Document(id={self.id}, filename={self.filename})"
