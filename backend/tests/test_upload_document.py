import pytest
from pathlib import Path
from io import BytesIO
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
EXAMPLES_DIR = Path(__file__).parent / "examples"


class TestDocumentUpload:

    def test_upload_and_process_clinical_history_complete_flow(self):
        """
        Scenario: Uploading a complete clinical history text file

        GIVEN a valid Spanish veterinary clinical history file
        WHEN the user uploads the document
        THEN the system should:
          1. Return a 200 OK status
          2. Extract the raw text correctly
          3. Parse the medical record into a structured JSON format
        """
        response = self._upload_example("clinical_history_1.txt")

        assert response.status_code == 200
        data = response.json()

        assert data["filename"] == "clinical_history_1.txt"
        assert data["file_type"] == "txt"
        assert "document_id" in data

        assert "BOS PARQUE OESTE" in data["extracted_text"]
        assert "Datos de la Mascota" in data["extracted_text"]

        record = data["medical_record"]
        assert record is not None

        assert record["veterinary_info"]["clinic_name"] == "BOS PARQUE OESTE"
        assert "AVDA EUROPA" in record["veterinary_info"]["clinic_address"]

        assert len(record["visits"]) > 0
        first_visit = record["visits"][0]
        assert first_visit["visit_date"].startswith("2019-12-08")

        assert first_visit["physical_examination"]["weight"] == 4.1

    @pytest.mark.parametrize(
        "filename, mime_type",
        [
            ("clinical_history.pdf", "application/pdf"),
            ("medical_scan.jpg", "image/jpeg"),
            ("medical_scan.png", "image/png"),
            ("medical_record.txt", "text/plain"),
            (
                "medical_report.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        ],
    )
    def test_upload_supported_file_types(self, filename, mime_type):
        """
        Scenario: Uploading different supported file types

        GIVEN a supported file (PDF, JPG, PNG, TXT, DOCX)
        WHEN uploaded
        THEN the system should accept it and extract text (using OCR for images)
        """
        if not (EXAMPLES_DIR / filename).exists():
            pytest.skip(f"Example file {filename} not found")

        response = self._upload_example(filename, mime_type)

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == filename
        assert data["extracted_text"] is not None
        if "scan" in filename or "history" in filename:
            assert len(data["extracted_text"]) > 0

    def test_upload_duplicate_files_creates_separate_entries(self):
        """
        Scenario: Uploading the same file twice

        GIVEN a file that has already been uploaded
        WHEN uploaded again
        THEN the system should create a new document entry with a unique ID
        """
        response1 = self._upload_example("medical_record.txt")
        response2 = self._upload_example("medical_record.txt")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["document_id"] != response2.json()["document_id"]

    def test_preserve_special_characters_in_filename(self):
        """
        Scenario: Filenames with special characters

        GIVEN a file with special characters in its name
        WHEN uploaded
        THEN the filename should be preserved exactly as is
        """
        special_name = "patient_ñame_José_#1.txt"
        content = b"Simple content"

        response = self._upload_content(special_name, content, "text/plain")

        assert response.status_code == 200
        assert response.json()["filename"] == special_name

    @pytest.mark.parametrize(
        "filename, mime_type",
        [
            ("malware.exe", "application/x-msdownload"),
            ("video.mp4", "video/mp4"),
            ("archive.zip", "application/zip"),
        ],
    )
    def test_reject_unsupported_file_types(self, filename, mime_type):
        """
        Scenario: Uploading unsupported file types

        GIVEN a file with an unsupported extension/type
        WHEN uploaded
        THEN the system should reject it with a 400 Bad Request
        """
        content = b"fake content"
        response = self._upload_content(filename, content, mime_type)

        assert response.status_code == 400
        assert "unsupported file type" in response.json()["detail"].lower()

    def test_reject_files_exceeding_size_limit(self):
        """
        Scenario: Uploading a file that is too large

        GIVEN a file larger than the allowed limit (e.g., 50MB)
        WHEN uploaded
        THEN the system should reject it with a 400 Bad Request
        """
        large_content = b"x" * (51 * 1024 * 1024)
        response = self._upload_content("huge.pdf", large_content, "application/pdf")

        assert response.status_code == 400
        assert "too large" in response.json()["detail"].lower()

    def test_reject_empty_files(self):
        """
        Scenario: Uploading an empty file

        GIVEN a file with 0 bytes
        WHEN uploaded
        THEN the system should reject it
        """
        response = self._upload_content("empty.txt", b"", "text/plain")

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    @pytest.mark.parametrize(
        "filename, mime_type",
        [
            ("corrupted.pdf", "application/pdf"),
            ("corrupted.jpg", "image/jpeg"),
            (
                "corrupted.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        ],
    )
    def test_handle_corrupted_files_gracefully(self, filename, mime_type):
        """
        Scenario: Uploading corrupted files

        GIVEN a corrupted file (invalid content for its type)
        WHEN uploaded
        THEN the system should accept the upload but handle the extraction failure gracefully
        (returning empty text instead of crashing)
        """
        if (EXAMPLES_DIR / filename).exists():
            response = self._upload_example(filename, mime_type)
        else:
            response = self._upload_content(filename, b"not a real file", mime_type)

        assert response.status_code == 200
        assert "extracted_text" in response.json()

    def _upload_example(self, filename: str, mime_type: str = None):
        file_path = EXAMPLES_DIR / filename

        if not mime_type:
            if filename.endswith(".pdf"):
                mime_type = "application/pdf"
            elif filename.endswith(".jpg"):
                mime_type = "image/jpeg"
            elif filename.endswith(".png"):
                mime_type = "image/png"
            elif filename.endswith(".txt"):
                mime_type = "text/plain"
            elif filename.endswith(".docx"):
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                mime_type = "application/octet-stream"

        with open(file_path, "rb") as f:
            content = f.read()

        return client.post(
            "/api/v1/document", files={"file": (filename, BytesIO(content), mime_type)}
        )

    def _upload_content(self, filename: str, content: bytes, mime_type: str):
        return client.post(
            "/api/v1/document", files={"file": (filename, BytesIO(content), mime_type)}
        )
