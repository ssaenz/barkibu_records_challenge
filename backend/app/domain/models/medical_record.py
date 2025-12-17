from dataclasses import dataclass, field
from typing import Optional
from app.domain.models.pet_info import PetInfo
from app.domain.models.veterinary_info import VeterinaryInfo
from app.domain.models.visit import Visit


@dataclass
class MedicalRecord:

    pet_info: Optional[PetInfo] = None
    veterinary_info: Optional[VeterinaryInfo] = None
    visits: list[Visit] = field(default_factory=list)
