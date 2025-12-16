"""Repository interfaces - Contracts for data access adapters"""
from abc import ABC, abstractmethod
from app.domain.models.document import Document


class DocumentRepository(ABC):
    """Interface for document storage and retrieval"""

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
