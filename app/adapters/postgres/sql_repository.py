from sqlalchemy.orm import Session
from app.domain.models.document import Document
from app.domain.repositories.document_repository import DocumentRepository
from app.adapters.postgres.schema.DocumentSchema import DocumentSchema


class SQLDocumentRepository(DocumentRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, document: Document) -> Document:
        orm = DocumentSchema.from_domain(document)
        self.db.add(orm)
        self.db.flush()
        self.db.commit()
        return document
