import spacy

from app.domain.medical_record_extractor import MedicalRecordExtractor
from app.domain.models.medical_record import MedicalRecord
from app.adapters.spacy.extractors.pet_info_extractor import PetInfoExtractor
from app.adapters.spacy.extractors.veterinary_info_extractor import (
    VeterinaryInfoExtractor,
)
from app.adapters.spacy.extractors.visit_extractor import VisitExtractor


class SpacyMedicalRecordExtractor(MedicalRecordExtractor):

    def __init__(self, model_name: str = "es_core_news_sm"):
        self.nlp = spacy.load(model_name)
        self._add_entity_ruler()

        self.pet_info_extractor = PetInfoExtractor(self.nlp)
        self.veterinary_info_extractor = VeterinaryInfoExtractor()
        self.visit_extractor = VisitExtractor(self.nlp)

    def _add_entity_ruler(self):
        ruler = self.nlp.add_pipe("entity_ruler", before="ner")

        patterns = [
            {"label": "SPECIES", "pattern": "perro"},
            {"label": "SPECIES", "pattern": "perra"},
            {"label": "SPECIES", "pattern": "gato"},
            {"label": "SPECIES", "pattern": "gata"},
            {"label": "SPECIES", "pattern": "conejo"},
            {"label": "SPECIES", "pattern": "hurón"},
            {"label": "SPECIES", "pattern": "loro"},
            {"label": "SYMPTOM", "pattern": "vómitos"},
            {"label": "SYMPTOM", "pattern": "diarrea"},
            {"label": "SYMPTOM", "pattern": "fiebre"},
            {"label": "SYMPTOM", "pattern": "tos"},
            {"label": "SYMPTOM", "pattern": "cojera"},
            {"label": "SYMPTOM", "pattern": "decaimiento"},
            {"label": "SYMPTOM", "pattern": "inapetencia"},
            {"label": "MEDICATION", "pattern": "amoxicilina"},
            {"label": "MEDICATION", "pattern": "meloxicam"},
            {"label": "MEDICATION", "pattern": "prednisona"},
            {"label": "MEDICATION", "pattern": "metronidazol"},
            {"label": "MEDICATION", "pattern": "enrofloxacino"},
        ]
        ruler.add_patterns(patterns)

    def extract(self, text: str) -> MedicalRecord:
        if not text or not text.strip():
            return MedicalRecord()

        doc = self.nlp(text)

        clinic_info = self.veterinary_info_extractor.extract(text)
        pet_info = self.pet_info_extractor.extract(doc, text)
        visits = self.visit_extractor.extract(doc, text)

        return MedicalRecord(
            pet_info=pet_info, veterinary_info=clinic_info, visits=visits
        )
