"""File repository interface - Contract for file storage adapters"""
from abc import ABC, abstractmethod


class FileRepository(ABC):
    """Interface for file storage operations"""

    @abstractmethod
    def upload(self, file_data: bytes, storage_key: str) -> dict:
        """
        Upload file to storage
        
        Args:
            file_data: File content as bytes
            storage_key: Unique key for storing the file
            
        Returns:
            Dictionary with storage details {bucket, key, size, etc}
        """
        pass
