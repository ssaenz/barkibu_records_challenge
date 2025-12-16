from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Text, LargeBinary
from app.adapters.postgres.database import Base
from app.domain.models.document import Document


class DocumentSchema(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    extracted_text = Column(Text, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"DocumentSchema(id={self.id}, filename={self.filename})"

    @staticmethod
    def from_domain(domain: Document) -> "DocumentSchema":
        orm = DocumentSchema()
        orm.id = domain.id
        orm.filename = domain.filename
        orm.file_type = domain.file_type
        orm.file_size = domain.file_size
        orm.file_data = domain.file_data
        orm.extracted_text = domain.extracted_text
        orm.created_at = domain.created_at
        orm.updated_at = domain.updated_at
        return orm
