from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, Union


@dataclass
class LaboratoryTest:

    test_name: str
    test_date: Optional[datetime] = None
    results: Optional[Union[str, dict[str, Any]]] = None
    findings: list[str] = field(default_factory=list)
