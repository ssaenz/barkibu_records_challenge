from dataclasses import dataclass
from typing import Optional


@dataclass
class VeterinaryInfo:

    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    clinic_phone: Optional[str] = None
