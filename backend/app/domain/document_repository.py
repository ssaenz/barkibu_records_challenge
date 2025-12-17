from abc import ABC, abstractmethod
from app.domain.models.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document: Document) -> Document:
        """
        Save a document

        Args:
            document: Domain Document object

        Returns:
            Saved Document object
        """
        pass

    @abstractmethod
    def get_by_id(self, document_id: str) -> Document:
        """
        Get a document by ID

        Args:
            document_id: Document ID

        Returns:
            Document object or None if not found
        """
        pass

    @abstractmethod
    def update(self, document: Document) -> Document:
        """
        Update a document

        Args:
            document: Domain Document object

        Returns:
            Updated Document object
        """
        pass
