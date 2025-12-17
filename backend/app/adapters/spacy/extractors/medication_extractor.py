from typing import List
from app.domain.models.medication import Medication
from app.adapters.spacy.extractors.utils import extract_section_text


class MedicationExtractor:
    def extract(self, text: str) -> List[Medication]:
        treatment_list = []
        treatment_text = extract_section_text(
            text, "(?:Tratamiento|Tx|Receta|Plan)", ["Revision", "Observaciones"]
        )
        if treatment_text:
            treats = [
                t.strip("- ").strip() for t in treatment_text.split("\n") if t.strip()
            ]
            for t in treats:
                treatment_list.append(Medication(name=t))
        return treatment_list
