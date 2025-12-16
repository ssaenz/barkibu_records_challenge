"""
Comprehensive test suite for POST /api/v1/documents endpoint

This test file covers all scenarios for document upload:
1. Successful uploads with real files (PDF, JPG, PNG, TXT, DOCX)
2. OCR text extraction verification
3. Error cases (corrupted files, invalid types, size limits)
4. Edge cases and validation
"""

import pytest
from pathlib import Path
from io import BytesIO
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.adapters.postgres.schema.DocumentSchema import DocumentSchema

client = TestClient(app)

# Test data directory
EXAMPLES_DIR = Path(__file__).parent / "examples"


class TestDocumentUploadEndpoint:
    """Test suite for POST /api/v1/documents endpoint"""

    # ==================== SUCCESSFUL UPLOADS WITH REAL FILES ====================

    def test_upload_real_pdf(self, db_session: Session):
        """
        GIVEN: A real PDF file
        WHEN: User uploads the PDF
        THEN: Document is created, stored in DB with extracted text
        """
        file_path = EXAMPLES_DIR / "clinical_history.pdf"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "clinical_history.pdf",
                    BytesIO(file_content),
                    "application/pdf",
                )
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        assert data["filename"] == "clinical_history.pdf"
        assert data["file_type"] == "pdf"
        assert data["file_size"] == len(file_content)
        assert data["file_size"] > 0
        assert "created_at" in data

        # Verify in database
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc is not None
        assert db_doc.file_data == file_content
        assert db_doc.extracted_text is not None
        assert (
            len(db_doc.extracted_text) > 100
        )  # Should have substantial extracted text

    def test_upload_real_jpg_image(self, db_session: Session):
        """
        GIVEN: A real JPG medical scan image
        WHEN: User uploads the JPG
        THEN: Document is created and OCR extracts visible text
        """
        file_path = EXAMPLES_DIR / "medical_scan.jpg"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={"file": ("medical_scan.jpg", BytesIO(file_content), "image/jpeg")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "medical_scan.jpg"
        assert data["file_type"] == "jpg"
        assert data["file_size"] == len(file_content)

        # Verify OCR extraction from image
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.file_data == file_content
        assert db_doc.extracted_text is not None
        # Should extract text from the image (MEDICAL IMAGING CENTER, etc.)
        assert len(db_doc.extracted_text) > 0

    def test_upload_real_png_image(self, db_session: Session):
        """
        GIVEN: A real PNG medical scan image
        WHEN: User uploads the PNG
        THEN: Document is created and stored correctly
        """
        file_path = EXAMPLES_DIR / "medical_scan.png"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={"file": ("medical_scan.png", BytesIO(file_content), "image/png")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "medical_scan.png"
        assert data["file_type"] == "png"
        assert data["file_size"] == len(file_content)

        # Verify in database
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.file_data == file_content

    def test_upload_real_txt_file(self, db_session: Session):
        """
        GIVEN: A real TXT medical record
        WHEN: User uploads the TXT file
        THEN: Document is created and text content is extracted
        """
        file_path = EXAMPLES_DIR / "medical_record.txt"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={"file": ("medical_record.txt", BytesIO(file_content), "text/plain")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "medical_record.txt"
        assert data["file_type"] == "txt"
        assert data["file_size"] == len(file_content)

        # Verify text extraction
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.file_data == file_content
        assert db_doc.extracted_text is not None
        # For TXT files, extracted text should match the content
        expected_text = file_content.decode("utf-8", errors="ignore")
        assert db_doc.extracted_text == expected_text

    def test_upload_real_docx_file(self, db_session: Session):
        """
        GIVEN: A real DOCX medical report
        WHEN: User uploads the DOCX file
        THEN: Document is created and text is extracted from Word document
        """
        file_path = EXAMPLES_DIR / "medical_report.docx"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "medical_report.docx",
                    BytesIO(file_content),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "medical_report.docx"
        assert data["file_type"] == "docx"
        assert data["file_size"] == len(file_content)

        # Verify DOCX text extraction
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.file_data == file_content
        assert db_doc.extracted_text is not None
        # Should contain text from the medical report
        assert (
            "Medical Report" in db_doc.extracted_text
            or "Jane Smith" in db_doc.extracted_text
        )

    # ==================== ERROR CASES: CORRUPTED FILES ====================

    def test_upload_corrupted_pdf_gracefully_handles_error(self, db_session: Session):
        """
        GIVEN: A corrupted PDF file
        WHEN: User uploads the corrupted PDF
        THEN: Document is created but OCR extraction returns empty string (graceful failure)
        """
        file_path = EXAMPLES_DIR / "corrupted.pdf"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={"file": ("corrupted.pdf", BytesIO(file_content), "application/pdf")},
        )

        # Should still accept the file (graceful degradation)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "corrupted.pdf"

        # OCR should have failed gracefully (empty extracted_text)
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.file_data == file_content  # File still stored
        assert db_doc.extracted_text == ""  # OCR failed gracefully

    def test_upload_corrupted_jpg_gracefully_handles_error(self, db_session: Session):
        """
        GIVEN: A corrupted JPG file
        WHEN: User uploads the corrupted JPG
        THEN: Document is created but OCR returns empty string
        """
        file_path = EXAMPLES_DIR / "corrupted.jpg"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={"file": ("corrupted.jpg", BytesIO(file_content), "image/jpeg")},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify graceful OCR failure
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.extracted_text == ""

    def test_upload_corrupted_docx_gracefully_handles_error(self, db_session: Session):
        """
        GIVEN: A corrupted DOCX file
        WHEN: User uploads the corrupted DOCX
        THEN: Document is created but text extraction returns empty string
        """
        file_path = EXAMPLES_DIR / "corrupted.docx"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "corrupted.docx",
                    BytesIO(file_content),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Verify graceful extraction failure
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.extracted_text == ""

    # ==================== ERROR CASES: INVALID FILE TYPES ====================

    def test_upload_unsupported_file_type_exe(self):
        """
        GIVEN: An unsupported file type (.exe)
        WHEN: User attempts to upload
        THEN: 400 Bad Request with error message
        """
        file_path = EXAMPLES_DIR / "malware.exe"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "malware.exe",
                    BytesIO(file_content),
                    "application/x-msdownload",
                )
            },
        )

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_upload_unsupported_file_type_mp4(self):
        """
        GIVEN: An unsupported file type (.mp4 video)
        WHEN: User attempts to upload
        THEN: 400 Bad Request
        """
        fake_video = b"fake mp4 content"

        response = client.post(
            "/api/v1/documents",
            files={"file": ("video.mp4", BytesIO(fake_video), "video/mp4")},
        )

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_upload_unsupported_file_type_zip(self):
        """
        GIVEN: An unsupported file type (.zip archive)
        WHEN: User attempts to upload
        THEN: 400 Bad Request
        """
        fake_zip = b"PK\x03\x04fake zip"

        response = client.post(
            "/api/v1/documents",
            files={"file": ("archive.zip", BytesIO(fake_zip), "application/zip")},
        )

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    # ==================== ERROR CASES: FILE SIZE LIMITS ====================

    def test_upload_file_exceeds_size_limit(self):
        """
        GIVEN: A file larger than 50MB
        WHEN: User attempts to upload
        THEN: 400 Bad Request with size limit error
        """
        # Create a file larger than 50MB
        large_content = b"x" * (51 * 1024 * 1024)  # 51MB

        response = client.post(
            "/api/v1/documents",
            files={
                "file": ("huge_file.pdf", BytesIO(large_content), "application/pdf")
            },
        )

        assert response.status_code == 400
        assert "too large" in response.json()["detail"].lower()

    def test_upload_empty_file(self):
        """
        GIVEN: An empty file (0 bytes)
        WHEN: User attempts to upload
        THEN: 400 Bad Request with error message
        """
        empty_content = b""

        response = client.post(
            "/api/v1/documents",
            files={"file": ("empty.txt", BytesIO(empty_content), "text/plain")},
        )

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    # ==================== EDGE CASES ====================

    def test_upload_file_with_special_characters_in_filename(self, db_session: Session):
        """
        GIVEN: A file with special characters in filename
        WHEN: User uploads the file
        THEN: Filename is preserved correctly
        """
        file_path = EXAMPLES_DIR / "medical_record.txt"
        with open(file_path, "rb") as f:
            file_content = f.read()

        special_filename = "patient_ñame_José_Müller_#1_@2025.txt"

        response = client.post(
            "/api/v1/documents",
            files={"file": (special_filename, BytesIO(file_content), "text/plain")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == special_filename

    def test_upload_same_file_twice_creates_different_documents(
        self, db_session: Session
    ):
        """
        GIVEN: The same file uploaded twice
        WHEN: User uploads the file two times
        THEN: Two separate documents are created with different IDs
        """
        file_path = EXAMPLES_DIR / "medical_record.txt"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response1 = client.post(
            "/api/v1/documents",
            files={"file": ("record.txt", BytesIO(file_content), "text/plain")},
        )
        response2 = client.post(
            "/api/v1/documents",
            files={"file": ("record.txt", BytesIO(file_content), "text/plain")},
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        doc1_id = response1.json()["document_id"]
        doc2_id = response2.json()["document_id"]

        # Different IDs for the same file uploaded twice
        assert doc1_id != doc2_id

        # Both should exist in database with identical content
        db_doc1 = db_session.query(DocumentSchema).filter_by(id=doc1_id).first()
        db_doc2 = db_session.query(DocumentSchema).filter_by(id=doc2_id).first()
        assert db_doc1.file_data == db_doc2.file_data

    def test_upload_large_but_valid_pdf(self, db_session: Session):
        """
        GIVEN: A large PDF file (clinical_history_large.pdf ~1.8MB)
        WHEN: User uploads the large PDF
        THEN: Document is created and processed successfully
        """
        file_path = EXAMPLES_DIR / "clinical_history_large.pdf"
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Verify it's actually a large file
        assert len(file_content) > 1_000_000  # > 1MB

        response = client.post(
            "/api/v1/documents",
            files={
                "file": ("large_clinical.pdf", BytesIO(file_content), "application/pdf")
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["file_size"] > 1_000_000

        # Verify stored correctly
        doc_id = data["document_id"]
        db_doc = db_session.query(DocumentSchema).filter_by(id=doc_id).first()
        assert db_doc.file_data == file_content
        assert db_doc.extracted_text is not None

    def test_response_format_matches_schema(self, db_session: Session):
        """
        GIVEN: Any valid document upload
        WHEN: Upload is successful
        THEN: Response matches expected schema with all required fields
        """
        file_path = EXAMPLES_DIR / "medical_record.txt"
        with open(file_path, "rb") as f:
            file_content = f.read()

        response = client.post(
            "/api/v1/documents",
            files={"file": ("test.txt", BytesIO(file_content), "text/plain")},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify all required fields are present
        required_fields = [
            "document_id",
            "filename",
            "file_type",
            "file_size",
            "created_at",
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Verify field types
        assert isinstance(data["document_id"], str)
        assert isinstance(data["filename"], str)
        assert isinstance(data["file_type"], str)
        assert isinstance(data["file_size"], int)
        assert isinstance(data["created_at"], str)

        # Verify UUID format for document_id
        import uuid

        try:
            uuid.UUID(data["document_id"])
        except ValueError:
            pytest.fail("document_id is not a valid UUID")
