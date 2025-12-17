export interface PetInfo {
  name?: string;
  species?: string;
  breed?: string;
  age?: string;
  weight?: string;
}

export interface VeterinaryInfo {
  name?: string;
  address?: string;
  phone?: string;
}

export interface PhysicalExamination {
  weight?: number;
  temperature?: number;
  heart_rate?: number;
  respiratory_rate?: number;
  mucous_membranes?: string;
  crt?: string;
  hydration_status?: string;
  general_condition?: string;
  abdominal_palpation?: string;
  findings?: string[];
}

export interface Medication {
  name: string;
  dosage?: string;
  frequency?: string;
  duration?: string;
  route?: string;
  observations?: string;
}

export interface LaboratoryTest {
  test_name: string;
  test_date?: string;
  results?: string | Record<string, any>;
  findings?: string[];
}

export interface Vaccination {
  vaccine_name: string;
  date_administered?: string;
  next_dose_date?: string;
  applied: boolean;
}

export interface Visit {
  visit_date?: string;
  visit_type?: string;
  clinic_name?: string;
  reason?: string;
  anamnesis?: string;
  physical_examination?: PhysicalExamination;
  diagnosis?: string[];
  treatment?: Medication[];
  plan?: string;
  laboratory_tests?: LaboratoryTest[];
  vaccinations?: Vaccination[];
  observations?: string;
}

export interface MedicalRecord {
  pet_info?: PetInfo;
  veterinary_info?: VeterinaryInfo;
  visits?: Visit[];
}

export interface DocumentResponse {
  document_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  extracted_text?: string;
  medical_record?: MedicalRecord;
  created_at: string;
}
