import pytest
import uuid
from pathlib import Path
from io import BytesIO
from fastapi.testclient import TestClient
from app.main import app
from app.adapters.postgres.schema.DocumentSchema import DocumentSchema

client = TestClient(app)
EXAMPLES_DIR = Path(__file__).parent / "examples"


class TestDocumentUpdate:

    def test_update_medical_record_successfully(self, db_session):
        """
        Scenario: Updating an existing document's medical record

        GIVEN an existing document in the database
        WHEN the user sends a PUT request with new medical record data
        THEN the system should:
          1. Return a 200 OK status
          2. Return the updated document structure
          3. Persist the changes (verified by the response)
        """
        # 1. Create a document directly in the DB
        document_id = self._create_document_in_db(db_session)

        # 2. Prepare new data
        new_medical_record = {
            "pet_info": {
                "name": "Updated Rex",
                "species": "Dog",
                "breed": "Labrador",
                "weight": 25.5,
            },
            "veterinary_info": {
                "clinic_name": "New Vet Clinic",
                "clinic_address": "123 New St",
            },
            "visits": [
                {
                    "visit_date": "2023-01-01T10:00:00",
                    "reason": "Checkup",
                    "diagnosis": ["Healthy"],
                    "treatment": [],
                }
            ],
        }

        # 3. Update the document
        response = self._update_document(document_id, new_medical_record)

        # 4. Verify response
        assert response.status_code == 200
        data = response.json()

        assert data["document_id"] == document_id
        assert data["medical_record"]["pet_info"]["name"] == "Updated Rex"
        assert (
            data["medical_record"]["veterinary_info"]["clinic_name"] == "New Vet Clinic"
        )
        assert len(data["medical_record"]["visits"]) == 1
        assert data["medical_record"]["visits"][0]["reason"] == "Checkup"

    def test_update_non_existent_document(self):
        """
        Scenario: Updating a document that does not exist

        GIVEN a non-existent document ID
        WHEN the user sends a PUT request
        THEN the system should return 404 Not Found
        """
        fake_id = "non-existent-id"
        new_medical_record = {"pet_info": {"name": "Ghost"}}

        response = self._update_document(fake_id, new_medical_record)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_with_invalid_data(self, db_session):
        """
        Scenario: Updating with invalid data types

        GIVEN an existing document
        WHEN the user sends invalid data (e.g., string for weight)
        THEN the system should return 422 Unprocessable Entity
        """
        document_id = self._create_document_in_db(db_session)

        invalid_record = {"pet_info": {"weight": "not-a-number"}}

        response = self._update_document(document_id, invalid_record)

        assert response.status_code == 422

    def _create_document_in_db(self, session) -> str:
        doc_id = str(uuid.uuid4())
        document = DocumentSchema(
            id=doc_id,
            filename="test_doc.txt",
            file_type="txt",
            file_size=100,
            file_data=b"test content",
            extracted_text="Initial text",
            medical_record_data={},
        )
        session.add(document)
        session.commit()
        return doc_id

    def _update_document(self, document_id: str, payload: dict):
        return client.put(f"/api/v1/document/{document_id}", json=payload)
