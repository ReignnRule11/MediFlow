"""
app/routers/medications.py - Medication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.schemas import MedicationResponse, PatientMedicationCreate, PatientMedicationResponse, PaginationParams, PaginatedResponse
from app.models import Medication, PatientMedication, User
from app.dependencies import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/medications", tags=["medications"])


@router.get("", response_model=PaginatedResponse)
async def list_medications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None, min_length=1),
    db: Session = Depends(get_db)
) -> PaginatedResponse:
    """List all medications with optional search"""
    try:
        query = db.query(Medication).filter(Medication.is_active == True)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Medication.generic_name.ilike(search_term),
                    Medication.brand_names.contains([search])
                )
            )

        total = query.count()
        medications = query.offset(skip).limit(limit).all()

        return PaginatedResponse(
            items=[MedicationResponse.from_orm(m) for m in medications],
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            total_pages=(total + limit - 1) // limit
        )

    except Exception as e:
        logger.error(f"List medications error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve medications"
        )


@router.get("/{medication_id}", response_model=MedicationResponse)
async def get_medication(
    medication_id: str,
    db: Session = Depends(get_db)
) -> MedicationResponse:
    """Get specific medication"""
    try:
        medication = db.query(Medication).filter(
            and_(
                Medication.id == medication_id,
                Medication.is_active == True
            )
        ).first()

        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication not found"
            )

        return MedicationResponse.from_orm(medication)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get medication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve medication"
        )


@router.get("/{medication_id}/interactions", response_model=list)
async def get_medication_interactions(
    medication_id: str,
    db: Session = Depends(get_db)
) -> list:
    """Get drug interactions for a medication"""
    try:
        medication = db.query(Medication).filter(Medication.id == medication_id).first()

        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication not found"
            )

        # This would typically query a drug_interactions table
        # For now, returning empty list
        return []

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get interactions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve interactions"
        )


@router.post("/patient/{patient_id}/medications", response_model=PatientMedicationResponse, status_code=status.HTTP_201_CREATED)
async def add_patient_medication(
    patient_id: str,
    med_data: PatientMedicationCreate,
    doctor_id: str = Query(...),
    db: Session = Depends(get_db)
) -> PatientMedicationResponse:
    """Add medication to patient"""
    try:
        # Verify patient exists
        patient = db.query(User).filter(User.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        # Verify medication exists
        medication = db.query(Medication).filter(Medication.id == med_data.medication_id).first()
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication not found"
            )

        # Create patient medication
        patient_med = PatientMedication(
            patient_id=patient_id,
            medication_id=med_data.medication_id,
            doctor_id=doctor_id,
            dose=med_data.dose,
            frequency=med_data.frequency,
            start_date=med_data.start_date,
            end_date=med_data.end_date,
            indication=med_data.indication,
            instructions=med_data.instructions
        )

        db.add(patient_med)
        db.commit()
        db.refresh(patient_med)

        logger.info(f"Added medication {med_data.medication_id} to patient {patient_id}")

        return PatientMedicationResponse.from_orm(patient_med)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Add medication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not add medication"
        )


@router.get("/patient/{patient_id}/active", response_model=list)
async def get_patient_active_medications(
    patient_id: str,
    db: Session = Depends(get_db)
) -> list:
    """Get patient's active medications"""
    try:
        # Verify patient exists
        patient = db.query(User).filter(User.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        medications = db.query(PatientMedication).filter(
            and_(
                PatientMedication.patient_id == patient_id,
                PatientMedication.status == "active",
                PatientMedication.deleted_at == None
            )
        ).all()

        return [PatientMedicationResponse.from_orm(m) for m in medications]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get patient medications error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve patient medications"
        )
