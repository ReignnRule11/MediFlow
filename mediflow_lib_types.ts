// lib/types.ts - Complete type definitions

export type UserRole = 'patient' | 'doctor' | 'admin' | 'caregiver';
export type MedicationStatus = 'active' | 'discontinued' | 'paused' | 'completed';
export type InteractionSeverity = 'minor' | 'moderate' | 'severe';
export type DocumentType = 'prescription' | 'lab_report' | 'discharge_summary' | 'imaging' | 'procedure_note';
export type ExtractionStatus = 'pending' | 'processing' | 'completed' | 'failed';
export type EventType = 'medication' | 'lab' | 'appointment' | 'vital' | 'note' | 'procedure';
export type EventSeverity = 'critical' | 'high' | 'medium' | 'low' | 'info';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  phone?: string;
  is_active: boolean;
  email_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthToken {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
  expires_in: number;
}

export interface Medication {
  id: string;
  name: string;
  generic_name: string;
  strength: string;
  frequency: string;
  dosage_form: string;
  start_date: string;
  end_date?: string;
  refills_remaining: number;
  status: MedicationStatus;
  adherence_score: number;
  source_document_id?: string;
}

export interface DrugInteraction {
  drug1_id: string;
  drug2_id: string;
  severity: InteractionSeverity;
  description: string;
  management_strategy: string;
}

export interface Patient {
  id: string;
  user_id: string;
  blood_type?: string;
  known_allergies: string[];
  chronic_conditions: string[];
  insurance_provider?: string;
  height_cm?: number;
  weight_kg?: number;
  bmi?: number;
}

export interface Document {
  id: string;
  patient_id: string;
  document_type: DocumentType;
  file_name: string;
  s3_url: string;
  extraction_status: ExtractionStatus;
  ocr_text?: string;
  ocr_confidence?: number;
  extracted_data?: ExtractedData;
  created_at: string;
}

export interface ExtractedData {
  medications?: ExtractedMedication[];
  labs?: ExtractedLab[];
  appointments?: ExtractedAppointment[];
  diagnoses?: string[];
}

export interface ExtractedMedication {
  name: string;
  strength: string;
  frequency: string;
  dosage_form: string;
  instructions?: string;
}

export interface ExtractedLab {
  test_name: string;
  value: number;
  unit: string;
  reference_range?: string;
  is_abnormal: boolean;
}

export interface ExtractedAppointment {
  doctor_name: string;
  date: string;
  time?: string;
  location?: string;
}

export interface TimelineEvent {
  id: string;
  patient_id: string;
  event_type: EventType;
  title: string;
  description?: string;
  event_date: string;
  severity: EventSeverity;
  is_abnormal: boolean;
  clinical_insight?: string;
  related_event_ids: string[];
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  message?: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
}

export interface CreateMedicationRequest {
  name: string;
  generic_name?: string;
  strength: string;
  dosage_form: string;
  frequency: string;
  start_date: string;
  end_date?: string;
  refills_remaining?: number;
}
