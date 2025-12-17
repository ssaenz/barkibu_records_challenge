from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any, Dict
from datetime import datetime
from app.domain.models.medical_record import MedicalRecord
from app.domain.models.pet_info import PetInfo
from app.domain.models.veterinary_info import VeterinaryInfo
from app.domain.models.visit import Visit
from app.domain.models.physical_examination import PhysicalExamination
from app.domain.models.medication import Medication
from app.domain.models.laboratory_test import LaboratoryTest
from app.domain.models.vaccination import Vaccination


class PetInfoDTO(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[datetime] = None
    sex: Optional[str] = None
    reproductive_status: Optional[str] = None
    weight: Optional[float] = None
    microchip: Optional[str] = None
    hair_type: Optional[str] = None
    coat_color: Optional[str] = None


class VeterinaryInfoDTO(BaseModel):
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    clinic_phone: Optional[str] = None


class PhysicalExaminationDTO(BaseModel):
    weight: Optional[float] = None
    temperature: Optional[float] = None
    heart_rate: Optional[float] = None
    respiratory_rate: Optional[float] = None
    mucous_membranes: Optional[str] = None
    crt: Optional[str] = None
    hydration_status: Optional[str] = None
    general_condition: Optional[str] = None
    abdominal_palpation: Optional[str] = None
    findings: List[str] = Field(default_factory=list)


class MedicationDTO(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    route: Optional[str] = None
    observations: Optional[str] = None


class LaboratoryTestDTO(BaseModel):
    test_name: str
    test_date: Optional[datetime] = None
    results: Optional[Union[str, Dict[str, Any]]] = None
    findings: List[str] = Field(default_factory=list)


class VaccinationDTO(BaseModel):
    vaccine_name: str
    date_administered: Optional[datetime] = None
    next_dose_date: Optional[datetime] = None
    applied: bool = False


class VisitDTO(BaseModel):
    visit_date: Optional[datetime] = None
    visit_type: Optional[str] = None
    clinic_name: Optional[str] = None
    reason: Optional[str] = None
    anamnesis: Optional[str] = None
    physical_examination: Optional[PhysicalExaminationDTO] = None
    diagnosis: List[str] = Field(default_factory=list)
    treatment: List[MedicationDTO] = Field(default_factory=list)
    plan: Optional[str] = None
    laboratory_tests: List[LaboratoryTestDTO] = Field(default_factory=list)
    vaccinations: List[VaccinationDTO] = Field(default_factory=list)
    observations: Optional[str] = None


class MedicalRecordDTO(BaseModel):
    pet_info: Optional[PetInfoDTO] = None
    veterinary_info: Optional[VeterinaryInfoDTO] = None
    visits: List[VisitDTO] = Field(default_factory=list)

    def to_domain(self) -> MedicalRecord:
        pet_info = None
        if self.pet_info:
            pet_info = PetInfo(
                name=self.pet_info.name,
                species=self.pet_info.species,
                breed=self.pet_info.breed,
                birth_date=self.pet_info.birth_date,
                sex=self.pet_info.sex,
                reproductive_status=self.pet_info.reproductive_status,
                weight=self.pet_info.weight,
                microchip=self.pet_info.microchip,
                hair_type=self.pet_info.hair_type,
                coat_color=self.pet_info.coat_color,
            )

        veterinary_info = None
        if self.veterinary_info:
            veterinary_info = VeterinaryInfo(
                clinic_name=self.veterinary_info.clinic_name,
                clinic_address=self.veterinary_info.clinic_address,
                clinic_phone=self.veterinary_info.clinic_phone,
            )

        visits = []
        for v in self.visits:
            phys_exam = None
            if v.physical_examination:
                phys_exam = PhysicalExamination(
                    weight=v.physical_examination.weight,
                    temperature=v.physical_examination.temperature,
                    heart_rate=v.physical_examination.heart_rate,
                    respiratory_rate=v.physical_examination.respiratory_rate,
                    mucous_membranes=v.physical_examination.mucous_membranes,
                    crt=v.physical_examination.crt,
                    hydration_status=v.physical_examination.hydration_status,
                    general_condition=v.physical_examination.general_condition,
                    abdominal_palpation=v.physical_examination.abdominal_palpation,
                    findings=v.physical_examination.findings,
                )

            treatments = []
            for t in v.treatment:
                treatments.append(
                    Medication(
                        name=t.name,
                        dosage=t.dosage,
                        frequency=t.frequency,
                        duration=t.duration,
                        route=t.route,
                        observations=t.observations,
                    )
                )

            lab_tests = []
            for l in v.laboratory_tests:
                lab_tests.append(
                    LaboratoryTest(
                        test_name=l.test_name,
                        test_date=l.test_date,
                        results=l.results,
                        findings=l.findings,
                    )
                )

            vaccinations = []
            for vac in v.vaccinations:
                vaccinations.append(
                    Vaccination(
                        vaccine_name=vac.vaccine_name,
                        date_administered=vac.date_administered,
                        next_dose_date=vac.next_dose_date,
                        applied=vac.applied,
                    )
                )

            visits.append(
                Visit(
                    visit_date=v.visit_date,
                    visit_type=v.visit_type,
                    clinic_name=v.clinic_name,
                    reason=v.reason,
                    anamnesis=v.anamnesis,
                    physical_examination=phys_exam,
                    diagnosis=v.diagnosis,
                    treatment=treatments,
                    plan=v.plan,
                    laboratory_tests=lab_tests,
                    vaccinations=vaccinations,
                    observations=v.observations,
                )
            )

        return MedicalRecord(
            pet_info=pet_info, veterinary_info=veterinary_info, visits=visits
        )
