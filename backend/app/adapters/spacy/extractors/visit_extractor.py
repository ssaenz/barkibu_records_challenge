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

        # Use named groups to identify what we matched
        visit_markers = [
            # Date and Time: = 08/12/19 - 16:12 -
            r"(?:^|\n)\s*[=-]\s*(?P<date_time>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*-\s*(?P<time>\d{1,2}:\d{2})",
            # Date only: = 08/12/19
            r"(?:^|\n)\s*[=-]\s*(?P<date_only>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            # Explicit header: VISITA DEL DIA 08/12/2019
            r"(?:^|\n)\s*VISITA.*DEL D[IÍ]A\s+(?P<date_explicit>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            # Numbered visit: Visita 1
            r"(?:^|\n)\s*(?:Visita|Consulta)\s+(?P<number>\d+)",
        ]

        found_sections = []
        for pattern in visit_markers:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                start = match.start()
                # Adjust start to skip the newline if it was matched
                if text[start] == "\n":
                    start += 1

                date_str = None
                time_str = None

                groups = match.groupdict()
                if groups.get("date_time"):
                    date_str = groups["date_time"]
                    time_str = groups.get("time")
                elif groups.get("date_only"):
                    date_str = groups["date_only"]
                elif groups.get("date_explicit"):
                    date_str = groups["date_explicit"]
                # For numbered visits, we don't have a date in the header

                found_sections.append(
                    {
                        "start": start,
                        "end_header": match.end(),
                        "date_str": date_str,
                        "time_str": time_str,
                        "full_match": match.group(0),
                    }
                )

        # Deduplicate and sort
        # If two matches start at the same position (ignoring whitespace/newlines), keep the longest one
        found_sections.sort(key=lambda x: x["start"])

        unique_sections = []
        if found_sections:
            current = found_sections[0]
            for next_section in found_sections[1:]:
                # If the next section starts within the current section's header, it's likely a sub-match or duplicate
                if next_section["start"] < current["end_header"]:
                    # Keep the one with the longer header (more specific match)
                    if (next_section["end_header"] - next_section["start"]) > (
                        current["end_header"] - current["start"]
                    ):
                        current = next_section
                else:
                    unique_sections.append(current)
                    current = next_section
            unique_sections.append(current)

        for i, section in enumerate(unique_sections):
            start = section["start"]
            # The content starts after the header
            content_start = section["end_header"]

            end = (
                unique_sections[i + 1]["start"]
                if i + 1 < len(unique_sections)
                else len(text)
            )
            section_text = text[content_start:end]

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
