from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PetInfo:

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
