import pytesseract
import logging
import time
import concurrent.futures
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
from app.domain.text_extractor import TextExtractor

logger = logging.getLogger(__name__)


class TesseractOCRAdapter(TextExtractor):
    def extract_text(self, file_data: bytes, file_type: str) -> str:
        try:
            start_time = time.time()
            logger.info(f"Starting OCR for file type: {file_type}")
            result = ""
            if file_type.lower() == "pdf":
                result = self._extract_from_pdf(file_data)
            elif file_type.lower() in ["jpg", "jpeg", "png"]:
                result = self._extract_from_image(file_data)
            elif file_type.lower() == "txt":
                result = file_data.decode("utf-8", errors="ignore")
            elif file_type.lower() == "docx":
                result = self._extract_from_docx(file_data)

            duration = time.time() - start_time
            logger.info(f"OCR completed for {file_type} in {duration:.2f} seconds")
            return result
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""

    def _extract_from_pdf(self, file_data: bytes) -> str:
        start_time = time.time()
        images = convert_from_bytes(file_data)
        logger.info(
            f"PDF converted to {len(images)} images in {time.time() - start_time:.2f} seconds"
        )

        def process_page(args):
            i, image = args
            page_start = time.time()
            text = pytesseract.image_to_string(image)
            logger.info(
                f"OCR for page {i+1} took {time.time() - page_start:.2f} seconds"
            )
            return text

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(process_page, enumerate(images)))

        return "\n".join(results).strip()

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
            raise Exception("python-docx not installed")
