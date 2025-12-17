import re
from typing import Optional, List

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from app.domain.models.visit import Visit
from app.domain.models.physical_examination import PhysicalExamination
from app.adapters.spacy.extractors.utils import (
    extract_regex_field,
    parse_date,
    extract_section_text,
)
from app.adapters.spacy.extractors.physical_examination_extractor import (
    PhysicalExaminationExtractor,
)
from app.adapters.spacy.extractors.medication_extractor import MedicationExtractor
from app.adapters.spacy.extractors.laboratory_test_extractor import (
    LaboratoryTestExtractor,
)


class VisitExtractor:
    def __init__(self, nlp: Language):
        self.nlp = nlp
        self.matcher = Matcher(self.nlp.vocab)
        self._add_patterns()
        self.physical_exam_extractor = PhysicalExaminationExtractor()
        self.medication_extractor = MedicationExtractor()
        self.laboratory_test_extractor = LaboratoryTestExtractor()

    def _add_patterns(self):
        weight_patterns = [
            [
                {"LOWER": "peso"},
                {"IS_PUNCT": True},
                {"LIKE_NUM": True},
                {"LOWER": {"IN": ["kg", "kgs", "kilos"]}},
            ],
        ]
        self.matcher.add("WEIGHT", weight_patterns)

        date_patterns = [
            [{"LOWER": "fecha"}, {"IS_PUNCT": True}, {"SHAPE": "dd/dd/dddd"}],
            [{"LOWER": "fecha"}, {"IS_PUNCT": True}, {"SHAPE": "dd-dd-dddd"}],
        ]
        self.matcher.add("DATE", date_patterns)

    def extract(self, doc: Doc, text: str) -> List[Visit]:
        visits = []

        visit_markers = [
            r"Visita\s+(\d+)",
            r"Consulta\s+(\d+)",
            r"VISITA.*DEL D[IÍ]A\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"[=-]\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*-\s*(\d{1,2}:\d{2})",
            r"[=-]\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        ]

        sections = []
        for pattern in visit_markers:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                date_str = match.group(1)
                time_str = match.group(2) if len(match.groups()) > 1 else None
                sections.append(
                    {
                        "start": match.start(),
                        "date_str": date_str,
                        "time_str": time_str,
                    }
                )

        sections.sort(key=lambda x: x["start"])

        for i, section in enumerate(sections):
            start = section["start"]
            end = sections[i + 1]["start"] if i + 1 < len(sections) else len(text)
            section_text = text[start:end]

            visit = self._parse_visit_section(
                section_text, section.get("date_str"), section.get("time_str")
            )
            if visit:
                visits.append(visit)

        return visits

    def _parse_visit_section(
        self, text: str, date_str: Optional[str] = None, time_str: Optional[str] = None
    ) -> Optional[Visit]:
        visit_date = None
        if date_str:
            visit_date = parse_date(date_str)

        reason = extract_regex_field(
            text,
            [
                r"(?:Motivo|Razón|Consulta por):\s*([^\n]+)",
                r"Consulta:\s*([^\n]+)",
                r"Acude (?:a consulta )?(?:para|por|de)\s*([^\n.]+)",
                r"Vienen de urgencias porque\s*([^\n.]+)",
            ],
        )

        anamnesis = extract_section_text(
            text, "Anamnesis", ["Exploracion", "Tratamiento", "Pruebas"]
        )

        exam_text = extract_section_text(
            text,
            "(?:Exploracion|EFG|Examen Fisico)",
            ["Tratamiento", "Pruebas", "Diagnostico"],
        )
        physical_exam = None
        if exam_text:
            physical_exam = self.physical_exam_extractor.extract(exam_text)

        weight_match = re.search(r"(\d+(?:[.,]\d+)?)\s*kg", text, re.IGNORECASE)
        if weight_match:
            if not physical_exam:
                physical_exam = PhysicalExamination()
            physical_exam.weight = float(weight_match.group(1).replace(",", "."))

        diagnosis_list = []
        diagnosis_text = extract_section_text(
            text, "(?:Diagnostico|Dx)", ["Tratamiento", "Pruebas"]
        )
        if diagnosis_text:
            diags = [
                d.strip("- ").strip() for d in diagnosis_text.split("\n") if d.strip()
            ]
            diagnosis_list.extend(diags)

        treatment_list = self.medication_extractor.extract(text)
        tests_list = self.laboratory_test_extractor.extract(text)

        plan = extract_section_text(text, "(?:Plan|Revision)", [])

        if (
            reason
            or diagnosis_list
            or treatment_list
            or physical_exam
            or tests_list
            or anamnesis
        ):
            return Visit(
                visit_date=visit_date,
                reason=reason,
                anamnesis=anamnesis,
                physical_examination=physical_exam,
                diagnosis=diagnosis_list,
                treatment=treatment_list,
                laboratory_tests=tests_list,
                plan=plan,
            )

        return None
