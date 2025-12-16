"""OCR Service interface - Contract for OCR adapters"""

from abc import ABC, abstractmethod


class OCRService(ABC):
    """Interface for Optical Character Recognition (OCR) operations"""

    @abstractmethod
    def extract_text(self, file_data: bytes, file_type: str) -> str:
        """
        Extract text from document using OCR

        Args:
            file_data: Raw file bytes
            file_type: File extension (pdf, jpg, png, etc.)

        Returns:
            Extracted text content
        """
        pass
