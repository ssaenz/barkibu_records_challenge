from app.domain.models.veterinary_info import VeterinaryInfo


class VeterinaryInfoExtractor:
    def extract(self, text: str) -> VeterinaryInfo:
        lines = text.split("\n")
        clinic_name = None
        clinic_address = None

        for line in lines[:5]:
            if line.strip() and not any(
                k in line.lower() for k in ["fecha", "datos", "historial"]
            ):
                if not clinic_name:
                    clinic_name = line.strip()
                elif not clinic_address:
                    clinic_address = line.strip()

        return VeterinaryInfo(clinic_name=clinic_name, clinic_address=clinic_address)
