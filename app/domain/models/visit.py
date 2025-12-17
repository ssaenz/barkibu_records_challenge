from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from app.domain.models.physical_examination import PhysicalExamination
from app.domain.models.medication import Medication
from app.domain.models.laboratory_test import LaboratoryTest
from app.domain.models.vaccination import Vaccination


@dataclass
class Visit:

    visit_date: Optional[datetime] = None
    visit_type: Optional[str] = None
    clinic_name: Optional[str] = None
    reason: Optional[str] = None
    anamnesis: Optional[str] = None
    physical_examination: Optional[PhysicalExamination] = None
    diagnosis: list[str] = field(default_factory=list)
    treatment: list[Medication] = field(default_factory=list)
    plan: Optional[str] = None
    laboratory_tests: list[LaboratoryTest] = field(default_factory=list)
    vaccinations: list[Vaccination] = field(default_factory=list)
    observations: Optional[str] = None
