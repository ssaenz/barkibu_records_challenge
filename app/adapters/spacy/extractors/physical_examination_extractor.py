import re
from app.domain.models.physical_examination import PhysicalExamination


class PhysicalExaminationExtractor:
    def extract(self, text: str) -> PhysicalExamination:
        exam = PhysicalExamination()

        weight_match = re.search(r"(\d+(?:[.,]\d+)?)\s*kg", text, re.IGNORECASE)
        if weight_match:
            exam.weight = float(weight_match.group(1).replace(",", "."))

        temp_match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:°C|ºC|Tº)", text, re.IGNORECASE)
        if temp_match:
            exam.temperature = float(temp_match.group(1).replace(",", "."))

        hr_match = re.search(r"(\d+)\s*(?:lpm|ppm)", text, re.IGNORECASE)
        if hr_match:
            exam.heart_rate = float(hr_match.group(1))

        exam.findings = [
            line.strip("- ").strip() for line in text.split("\n") if line.strip()
        ]

        return exam
