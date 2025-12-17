from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PhysicalExamination:

    weight: Optional[float] = None
    temperature: Optional[float] = None
    heart_rate: Optional[float] = None
    respiratory_rate: Optional[float] = None
    mucous_membranes: Optional[str] = None
    crt: Optional[str] = None
    hydration_status: Optional[str] = None
    general_condition: Optional[str] = None
    abdominal_palpation: Optional[str] = None
    findings: list[str] = field(default_factory=list)
