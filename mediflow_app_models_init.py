"""
app/models/__init__.py - SQLAlchemy models
"""

from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, Enum as SQLEnum, Text, JSONB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

Base = declarative_base()


class UserRole(str, enum.Enum):
    """User role enumeration"""
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"
    CAREGIVER = "caregiver"


class MedicationStatus(str, enum.Enum):
    """Medication status enumeration"""
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    PAUSED = "paused"
    COMPLETED = "completed"


class DocumentType(str, enum.Enum):
    """Document type enumeration"""
    PRESCRIPTION = "prescription"
    LAB_REPORT = "lab_report"
    DISCHARGE_SUMMARY = "discharge_summary"
    IMAGING = "imaging"
    PROCEDURE_NOTE = "procedure_note"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(500), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.PATIENT, index=True)
    is_active = Column(Boolean, default=True, index=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Medication(Base):
    """Medication model"""
    __tablename__ = "medications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    generic_name = Column(String(255), nullable=False, index=True)
    brand_names = Column(JSONB, default=[])
    rxcui = Column(String(50), nullable=True, index=True)
    ndc_code = Column(String(50), nullable=True)
    strength = Column(String(100), nullable=False)
    dosage_form = Column(String(100), nullable=False)
    route_of_administration = Column(String(100), nullable=False)
    drug_class = Column(String(255), nullable=True, index=True)
    contraindications = Column(JSONB, default=[])
    warnings = Column(JSONB, default=[])
    side_effects = Column(JSONB, default=[])
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Medication {self.generic_name}>"


class PatientMedication(Base):
    """Patient medication model"""
    __tablename__ = "patient_medications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    medication_id = Column(String, ForeignKey("medications.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("users.id"), nullable=False)
    dose = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    refills_allowed = Column(Integer, nullable=True)
    refills_remaining = Column(Integer, nullable=True)
    indication = Column(String(500), nullable=True)
    instructions = Column(Text, nullable=True)
    status = Column(SQLEnum(MedicationStatus), default=MedicationStatus.ACTIVE, index=True)
    adherence_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<PatientMedication {self.patient_id}:{self.medication_id}>"


class Document(Base):
    """Document model"""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    document_type = Column(SQLEnum(DocumentType), nullable=False, index=True)
    file_name = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    s3_bucket = Column(String(255), nullable=True)
    s3_key = Column(String(1000), nullable=True)
    s3_url = Column(String(1000), nullable=True)
    file_hash = Column(String(64), nullable=True)
    extraction_status = Column(String(50), default="pending", index=True)
    ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)
    extracted_data = Column(JSONB, nullable=True)
    is_processed = Column(Boolean, default=False, index=True)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Document {self.file_name}>"


class Appointment(Base):
    """Appointment model"""
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    doctor_id = Column(String, ForeignKey("users.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False, index=True)
    appointment_type = Column(String(100), nullable=False)
    status = Column(String(50), default="scheduled", index=True)
    chief_complaint = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Appointment {self.id}>"
