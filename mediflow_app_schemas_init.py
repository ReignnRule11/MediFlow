"""
app/schemas/__init__.py - Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    """User role enumeration"""
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"
    CAREGIVER = "caregiver"


class MedicationStatus(str, Enum):
    """Medication status enumeration"""
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    PAUSED = "paused"
    COMPLETED = "completed"


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = None
    role: UserRole = UserRole.PATIENT


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('Password must contain special character')
        return v


class UserResponse(UserBase):
    """User response schema"""
    id: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


# Medication Schemas
class MedicationBase(BaseModel):
    """Base medication schema"""
    generic_name: str = Field(..., min_length=1, max_length=255)
    strength: str = Field(..., min_length=1, max_length=100)
    dosage_form: str = Field(..., min_length=1, max_length=100)


class MedicationResponse(MedicationBase):
    """Medication response schema"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PatientMedicationCreate(BaseModel):
    """Patient medication creation schema"""
    medication_id: str
    dose: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., min_length=1, max_length=100)
    start_date: datetime
    end_date: Optional[datetime] = None
    indication: Optional[str] = None
    instructions: Optional[str] = None


class PatientMedicationResponse(BaseModel):
    """Patient medication response schema"""
    id: str
    medication_id: str
    dose: str
    frequency: str
    start_date: datetime
    end_date: Optional[datetime]
    status: MedicationStatus
    adherence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


# Document Schemas
class DocumentType(str, Enum):
    """Document type enumeration"""
    PRESCRIPTION = "prescription"
    LAB_REPORT = "lab_report"
    DISCHARGE_SUMMARY = "discharge_summary"
    IMAGING = "imaging"
    PROCEDURE_NOTE = "procedure_note"


class DocumentUploadRequest(BaseModel):
    """Document upload request schema"""
    document_type: DocumentType


class DocumentResponse(BaseModel):
    """Document response schema"""
    id: str
    document_type: DocumentType
    file_name: str
    extraction_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Appointment Schemas
class AppointmentCreate(BaseModel):
    """Appointment creation schema"""
    doctor_id: str
    appointment_date: datetime
    appointment_type: str
    chief_complaint: Optional[str] = None


class AppointmentResponse(BaseModel):
    """Appointment response schema"""
    id: str
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    appointment_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Generic Schemas
class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int


class ApiResponse(BaseModel):
    """API response wrapper"""
    success: bool
    data: Optional[dict] = None
    error: Optional[dict] = None
    message: Optional[str] = None
