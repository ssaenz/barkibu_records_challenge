from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Vaccination:

    vaccine_name: str
    date_administered: Optional[datetime] = None
    next_dose_date: Optional[datetime] = None
    applied: bool = False
