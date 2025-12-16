"""Tesseract OCR Adapter - Implementation of TextExtractor using Tesseract"""

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
from app.domain.text_extractor import TextExtractor


class TesseractOCRAdapter(TextExtractor):
    def extract_text(self, file_data: bytes, file_type: str) -> str:
        try:
            if file_type.lower() == "pdf":
                return self._extract_from_pdf(file_data)
            elif file_type.lower() in ["jpg", "jpeg", "png"]:
                return self._extract_from_image(file_data)
            elif file_type.lower() == "txt":
                return file_data.decode("utf-8", errors="ignore")
            elif file_type.lower() == "docx":
                return self._extract_from_docx(file_data)
            else:
                # Unsupported file type - return empty string
                return ""
        except Exception as e:
            # OCR failed - return empty string instead of crashing
            # This allows the document to be stored even if OCR fails
            return ""

    def _extract_from_pdf(self, file_data: bytes) -> str:
        images = convert_from_bytes(file_data)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        return text.strip()

    def _extract_from_image(self, file_data: bytes) -> str:
        image = Image.open(BytesIO(file_data))
        return pytesseract.image_to_string(image)

    def _extract_from_docx(self, file_data: bytes) -> str:
        try:
            from docx import Document

            doc = Document(BytesIO(file_data))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except ImportError:
            raise Exception(
                "python-docx not installed. Install with: pip install python-docx"
            )
