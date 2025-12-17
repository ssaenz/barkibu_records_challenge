from sqlalchemy.orm import Session
from app.domain.models.document import Document
from app.domain.document_repository import DocumentRepository
from app.adapters.postgres.schema.DocumentSchema import DocumentSchema


class SQLDocumentRepository(DocumentRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, document: Document) -> Document:
        orm = DocumentSchema.from_domain(document)
        self.db.add(orm)
        self.db.flush()
        self.db.commit()
        return document

    def get_by_id(self, document_id: str) -> Document:
        orm = (
            self.db.query(DocumentSchema)
            .filter(DocumentSchema.id == document_id)
            .first()
        )
        if not orm:
            return None

        # Map ORM to Domain
        # We need to reconstruct the domain object from the ORM object
        # Since DocumentSchema stores medical_record as JSON, we need to deserialize it back to dataclasses
        # For now, let's assume we can just pass the dict if the domain model supports it,
        # but the domain model uses dataclasses.
        # We need a deserializer.

        # Let's implement a simple deserializer here or in DocumentSchema
        # For now, I'll do it here for simplicity, but ideally it should be in a mapper.

        from app.domain.models.document import Document
        from app.domain.models.medical_record import MedicalRecord
        from app.domain.models.pet_info import PetInfo
        from app.domain.models.veterinary_info import VeterinaryInfo
        from app.domain.models.visit import Visit
        from app.domain.models.physical_examination import PhysicalExamination
        from app.domain.models.medication import Medication
        from app.domain.models.laboratory_test import LaboratoryTest
        from app.domain.models.vaccination import Vaccination
        from datetime import datetime

        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.fromisoformat(date_str)
            except ValueError:
                return None

        medical_record = None
        if orm.medical_record_data:
            data = orm.medical_record_data

            pet_info = None
            if data.get("pet_info"):
                p = data["pet_info"]
                pet_info = PetInfo(
                    name=p.get("name"),
                    species=p.get("species"),
                    breed=p.get("breed"),
                    birth_date=parse_date(p.get("birth_date")),
                    sex=p.get("sex"),
                    reproductive_status=p.get("reproductive_status"),
                    weight=p.get("weight"),
                    microchip=p.get("microchip"),
                    hair_type=p.get("hair_type"),
                    coat_color=p.get("coat_color"),
                )

            veterinary_info = None
            if data.get("veterinary_info"):
                v = data["veterinary_info"]
                veterinary_info = VeterinaryInfo(
                    clinic_name=v.get("clinic_name"),
                    clinic_address=v.get("clinic_address"),
                    clinic_phone=v.get("clinic_phone"),
                )

            visits = []
            if data.get("visits"):
                for v in data["visits"]:
                    phys_exam = None
                    if v.get("physical_examination"):
                        pe = v["physical_examination"]
                        phys_exam = PhysicalExamination(
                            weight=pe.get("weight"),
                            temperature=pe.get("temperature"),
                            heart_rate=pe.get("heart_rate"),
                            respiratory_rate=pe.get("respiratory_rate"),
                            mucous_membranes=pe.get("mucous_membranes"),
                            crt=pe.get("crt"),
                            hydration_status=pe.get("hydration_status"),
                            general_condition=pe.get("general_condition"),
                            abdominal_palpation=pe.get("abdominal_palpation"),
                            findings=pe.get("findings", []),
                        )

                    treatments = []
                    if v.get("treatment"):
                        for t in v["treatment"]:
                            treatments.append(
                                Medication(
                                    name=t.get("name"),
                                    dosage=t.get("dosage"),
                                    frequency=t.get("frequency"),
                                    duration=t.get("duration"),
                                    route=t.get("route"),
                                    observations=t.get("observations"),
                                )
                            )

                    lab_tests = []
                    if v.get("laboratory_tests"):
                        for l in v["laboratory_tests"]:
                            lab_tests.append(
                                LaboratoryTest(
                                    test_name=l.get("test_name"),
                                    test_date=parse_date(l.get("test_date")),
                                    results=l.get("results"),
                                    findings=l.get("findings", []),
                                )
                            )

                    vaccinations = []
                    if v.get("vaccinations"):
                        for vac in v["vaccinations"]:
                            vaccinations.append(
                                Vaccination(
                                    vaccine_name=vac.get("vaccine_name"),
                                    date_administered=parse_date(
                                        vac.get("date_administered")
                                    ),
                                    next_dose_date=parse_date(
                                        vac.get("next_dose_date")
                                    ),
                                    applied=vac.get("applied", False),
                                )
                            )

                    visits.append(
                        Visit(
                            visit_date=parse_date(v.get("visit_date")),
                            visit_type=v.get("visit_type"),
                            clinic_name=v.get("clinic_name"),
                            reason=v.get("reason"),
                            anamnesis=v.get("anamnesis"),
                            physical_examination=phys_exam,
                            diagnosis=v.get("diagnosis", []),
                            treatment=treatments,
                            plan=v.get("plan"),
                            laboratory_tests=lab_tests,
                            vaccinations=vaccinations,
                            observations=v.get("observations"),
                        )
                    )

            medical_record = MedicalRecord(
                pet_info=pet_info, veterinary_info=veterinary_info, visits=visits
            )

        return Document(
            id=orm.id,
            filename=orm.filename,
            file_type=orm.file_type,
            file_size=orm.file_size,
            file_data=orm.file_data,
            extracted_text=orm.extracted_text,
            medical_record=medical_record,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def update(self, document: Document) -> Document:
        orm = (
            self.db.query(DocumentSchema)
            .filter(DocumentSchema.id == document.id)
            .first()
        )
        if orm:
            # Update fields
            orm.extracted_text = document.extracted_text

            # Serialize MedicalRecord
            from app.adapters.postgres.schema.DocumentSchema import serialize_dataclass

            orm.medical_record_data = (
                serialize_dataclass(document.medical_record)
                if document.medical_record
                else None
            )

            # Update timestamp handled by onupdate in schema, but we can force it if needed
            # orm.updated_at = datetime.now(timezone.utc)

            self.db.commit()
            self.db.refresh(orm)
        return document
