import pytest
from io import BytesIO
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestDocumentUpload:
    def test_upload_pdf_file(self):
        """
        Test 1.1: Upload PDF file
        WHEN: User uploads a valid PDF file
        THEN: Document created with status="uploaded"
        """
        # Create a simple PDF file for testing
        pdf_content = b"%PDF-1.4\nTest PDF content"

        response = client.post(
            "/api/v1/documents",
            files={
                "file": ("test_document.pdf", BytesIO(pdf_content), "application/pdf")
            },
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        assert data["filename"] == "test_document.pdf"
        assert data["file_type"] == "pdf"
        assert data["file_size"] == len(pdf_content)
        assert "path" in data
        assert "created_at" in data

    def test_upload_jpg_image(self):
        """
        Test 1.2: Upload JPG image
        WHEN: User uploads a JPG image
        THEN: Document created with file_type="jpg"
        """
        jpg_content = b"\xff\xd8\xff\xe0" + b"fake jpg content"

        response = client.post(
            "/api/v1/documents",
            files={"file": ("scan.jpg", BytesIO(jpg_content), "image/jpeg")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["file_type"] == "jpg"
        assert "path" in data

    def test_upload_docx_file(self):
        """
        Test 1.3: Upload Word document
        WHEN: User uploads a DOCX file
        THEN: Document created with file_type="docx"
        """
        docx_content = b"PK\x03\x04" + b"fake docx content"

        response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "report.docx",
                    BytesIO(docx_content),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["file_type"] == "docx"

    def test_upload_txt_file(self):
        """
        Test 1.4: Upload plain text file
        WHEN: User uploads a TXT file
        THEN: Document created with file_type="txt"
        """
        txt_content = b"This is a plain text medical record"

        response = client.post(
            "/api/v1/documents",
            files={"file": ("record.txt", BytesIO(txt_content), "text/plain")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["file_type"] == "txt"

    def test_upload_invalid_file_type(self):
        """
        Test 1.5: Upload unsupported file type
        WHEN: User uploads .exe file
        THEN: 400 Bad Request with error message
        """
        exe_content = b"MZ\x90\x00"  # Fake executable

        response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "malware.exe",
                    BytesIO(exe_content),
                    "application/x-msdownload",
                )
            },
        )

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_upload_file_too_large(self):
        """
        Test 1.6: Upload file exceeding size limit
        WHEN: User uploads file > 50MB
        THEN: 413 Payload Too Large
        """
        # Create a file larger than 50MB limit
        large_content = b"x" * (51 * 1024 * 1024)  # 51MB

        response = client.post(
            "/api/v1/documents",
            files={
                "file": ("large_file.pdf", BytesIO(large_content), "application/pdf")
            },
        )

        assert response.status_code == 400
        assert "too large" in response.json()["detail"].lower()

    def test_upload_multiple_files_different_types(self):
        """
        Test: Upload multiple documents in sequence
        WHEN: User uploads PDF, then JPG, then DOCX
        THEN: All stored separately with different IDs
        """
        pdf_content = b"%PDF-1.4\nTest"
        jpg_content = b"\xff\xd8\xff\xe0Test"
        docx_content = b"PK\x03\x04Test"

        # Upload PDF
        pdf_response = client.post(
            "/api/v1/documents",
            files={"file": ("doc1.pdf", BytesIO(pdf_content), "application/pdf")},
        )
        pdf_id = pdf_response.json()["document_id"]

        # Upload JPG
        jpg_response = client.post(
            "/api/v1/documents",
            files={"file": ("doc2.jpg", BytesIO(jpg_content), "image/jpeg")},
        )
        jpg_id = jpg_response.json()["document_id"]

        # Upload DOCX
        docx_response = client.post(
            "/api/v1/documents",
            files={
                "file": (
                    "doc3.docx",
                    BytesIO(docx_content),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
        docx_id = docx_response.json()["document_id"]

        # Verify all have different IDs
        assert pdf_id != jpg_id
        assert jpg_id != docx_id
        assert pdf_id != docx_id
