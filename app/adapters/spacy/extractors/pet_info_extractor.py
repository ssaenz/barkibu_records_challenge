import re
from datetime import datetime
from typing import Optional, List

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from app.domain.models.pet_info import PetInfo
from app.adapters.spacy.extractors.utils import extract_regex_field


class PetInfoExtractor:
    def __init__(self, nlp: Language):
        self.nlp = nlp
        self.matcher = Matcher(self.nlp.vocab)
        self._add_patterns()

    def _add_patterns(self):
        name_patterns = [
            [
                {"LOWER": {"IN": ["nombre", "paciente"]}},
                {"IS_PUNCT": True},
                {"IS_ALPHA": True, "OP": "+"},
            ],
            [
                {"LOWER": {"IN": ["nombre", "paciente"]}},
                {"IS_PUNCT": True},
                {"IS_SPACE": True, "OP": "?"},
                {"IS_ALPHA": True, "OP": "+"},
            ],
        ]
        self.matcher.add("PET_NAME", name_patterns)

        species_patterns = [
            [{"LOWER": "especie"}, {"IS_PUNCT": True}, {"IS_ALPHA": True}],
            [{"LOWER": {"IN": ["perro", "gato", "conejo", "hurón", "loro", "ave"]}}],
        ]
        self.matcher.add("SPECIES", species_patterns)

    def extract(self, doc: Doc, text: str) -> PetInfo:
        pet_name = self._extract_pet_name(doc, text)
        species = self._extract_species(doc, text)
        breed = extract_regex_field(
            text, [r"Raza:\s*([^\n]+)", r"CANINA\s*-\s*([^\n]+)"]
        )
        birth_date_str = extract_regex_field(
            text, [r"Nacimiento:\s*(\d{2}/\d{2}/\d{4})"]
        )
        birth_date = (
            datetime.strptime(birth_date_str, "%d/%m/%Y") if birth_date_str else None
        )
        sex = extract_regex_field(text, [r"Sexo:\s*(\w+)"])
        status = extract_regex_field(text, [r"Estado:\s*(\w+)"])
        microchip = extract_regex_field(text, [r"Chip:\s*([A-Z0-9\s]+)"])
        hair = extract_regex_field(text, [r"Pelo:\s*(\w+)"])
        coat = extract_regex_field(text, [r"Capa:\s*(\w+)"])

        return PetInfo(
            name=pet_name,
            species=species,
            breed=breed,
            birth_date=birth_date,
            sex=sex,
            reproductive_status=status,
            microchip=microchip,
            hair_type=hair,
            coat_color=coat,
        )

    def _extract_pet_name(self, doc: Doc, text: str) -> Optional[str]:
        matches = self.matcher(doc, as_spans=True)
        for span in matches:
            if span.label_ == "PET_NAME":
                name_text = span.text.split(":")[-1].strip()
                if name_text:
                    return name_text

        patterns = [
            r"(?:Nombre|Paciente|Mascota):\s*([A-Za-zÁÉÍÓÚáéíóúñÑ]+)",
            r"^([A-Za-zÁÉÍÓÚáéíóúñÑ]+)\s*[-–]\s*(?:perro|gato|conejo)",
            r"^([A-ZÁÉÍÓÚÑ]+)\s*-\s*Nacimiento",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()

        return None

    def _extract_species(self, doc: Doc, text: str) -> Optional[str]:
        for ent in doc.ents:
            if ent.label_ == "SPECIES":
                return ent.text.capitalize()

        patterns = [
            r"(?:Especie|Tipo):\s*(perro|perra|gato|gata|conejo|hurón|loro)",
            r"\b(perro|perra|gato|gata|conejo|hurón|loro)\b",
            r"(CANINA|FELINA)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                species = match.group(1).lower()
                if species in ["perro", "perra", "canina"]:
                    return "Canine"
                elif species in ["gato", "gata", "felina"]:
                    return "Feline"
                else:
                    return species.capitalize()

        return None
