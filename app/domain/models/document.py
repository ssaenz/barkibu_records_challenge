"""Core domain models - Pure Python objects, no external dependencies"""
from datetime import datetime, timezone
from typing import Optional


class Document:

    def __init__(
        self,
        id: str,
        filename: str,
        file_type: str,
        file_size: int,
        path: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.filename = filename
        self.file_type = file_type
        self.file_size = file_size
        self.path = path
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"Document(id={self.id}, filename={self.filename})"
