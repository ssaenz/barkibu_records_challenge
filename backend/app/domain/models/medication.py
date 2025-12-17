from dataclasses import dataclass
from typing import Optional


@dataclass
class Medication:

    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    route: Optional[str] = None
    observations: Optional[str] = None
