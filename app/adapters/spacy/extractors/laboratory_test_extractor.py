import re
from typing import List
from app.domain.models.laboratory_test import LaboratoryTest


class LaboratoryTestExtractor:
    def extract(self, text: str) -> List[LaboratoryTest]:
        tests_list = []
        test_lines = re.findall(
            r"(Test|Analitica|Radiografia|Ecografia|Coprologico).*?[:\n](.*)",
            text,
            re.IGNORECASE,
        )
        for test_name, test_result in test_lines:
            tests_list.append(
                LaboratoryTest(test_name=test_name.strip(), results=test_result.strip())
            )
        return tests_list
