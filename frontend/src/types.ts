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

export interface Visit {
  date?: string;
  reason?: string;
  diagnosis?: string;
  treatment?: string;
  notes?: string;
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
