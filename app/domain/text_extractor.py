"""Text Extractor interface - Contract for text extraction implementations"""

from abc import ABC, abstractmethod


class TextExtractor(ABC):
    """Interface for extracting text from documents"""

    @abstractmethod
    def extract_text(self, file_data: bytes, file_type: str) -> str:
        """
        Extract text from document

        Args:
            file_data: Raw file bytes
            file_type: File extension (pdf, jpg, png, etc.)

        Returns:
            Extracted text content
        """
        pass
