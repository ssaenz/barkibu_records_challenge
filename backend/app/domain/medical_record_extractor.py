from abc import ABC, abstractmethod
from app.domain.models.medical_record import MedicalRecord


class MedicalRecordExtractor(ABC):

    @abstractmethod
    def extract(self, text: str) -> MedicalRecord:
        """
        Extract structured medical record from raw text.

        Args:
            text: Raw text extracted from a medical document (via OCR or other means)

        Returns:
            MedicalRecord: Structured medical record with pet info, visits, treatments, etc.
        """
        pass
