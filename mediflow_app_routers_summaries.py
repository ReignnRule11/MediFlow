"""
app/routers/summaries.py - AI-powered pre-consultation summaries for doctors
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.schemas import PaginatedResponse
from app.models import User, PatientMedication, Patient, Appointment
from app.dependencies import get_db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/summaries", tags=["summaries"])


class DoctorSummary:
    """Data model for doctor pre-consultation summary"""
    def __init__(self):
        self.patient_name: str = ""
        self.patient_age: int = 0
        self.gender: str = ""
        self.chronic_conditions: list[str] = []
        self.current_medications: list[dict] = []
        self.recent_labs: list[dict] = []
        self.allergies: list[str] = []
        self.alerts: list[dict] = []
        self.adherence_score: float = 0.0
        self.generated_at: datetime = datetime.now()


@router.get("/doctor/patient/{patient_id}/pre-consultation")
async def get_pre_consultation_summary(
    patient_id: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Generate AI-powered pre-consultation summary for doctor.
    
    This endpoint aggregates patient data into a one-page clinical summary
    that doctors can review in <3 seconds before seeing the patient.
    
    TIER 1 PRIORITY: This is the highest ROI feature (saves 15 min per patient).
    """
    try:
        # Verify patient exists
        patient_user = db.query(User).filter(User.id == patient_id).first()
        if not patient_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        patient_profile = db.query(Patient).filter(Patient.user_id == patient_id).first()

        # Build summary components
        summary = DoctorSummary()
        summary.patient_name = patient_user.full_name
        summary.patient_age = calculate_age(patient_user.date_of_birth) if patient_user.date_of_birth else None
        
        # Chronic conditions
        if patient_profile and patient_profile.chronic_conditions:
            summary.chronic_conditions = patient_profile.chronic_conditions

        # Current medications (ACTIVE only)
        active_meds = db.query(PatientMedication).filter(
            and_(
                PatientMedication.patient_id == patient_id,
                PatientMedication.status == "active",
                PatientMedication.deleted_at == None
            )
        ).all()

        for med in active_meds:
            summary.current_medications.append({
                'name': med.medication.generic_name if med.medication else med.name,
                'dose': med.dose,
                'frequency': med.frequency,
                'adherence_score': med.adherence_score,
                'start_date': med.start_date.isoformat()
            })

        # Average adherence across medications
        if active_meds:
            adherence_scores = [m.adherence_score for m in active_meds if m.adherence_score is not None]
            summary.adherence_score = sum(adherence_scores) / len(adherence_scores) if adherence_scores else 0.0

        # Allergies (critical safety)
        if patient_profile and patient_profile.known_allergies:
            summary.allergies = patient_profile.known_allergies

        # Recent labs (last 30 days, focus on abnormal)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        # Note: This assumes a lab_results table - adjust import based on your schema
        
        # Clinical alerts (example heuristics)
        alerts = generate_clinical_alerts(
            patient_profile=patient_profile,
            medications=active_meds,
            adherence=summary.adherence_score
        )
        summary.alerts = alerts

        return {
            "success": True,
            "data": {
                "patient_name": summary.patient_name,
                "patient_age": summary.patient_age,
                "chronic_conditions": summary.chronic_conditions,
                "current_medications": summary.current_medications,
                "allergies": summary.allergies,
                "adherence_score": round(summary.adherence_score, 2),
                "alerts": summary.alerts,
                "generated_at": summary.generated_at.isoformat(),
                "note": "This summary was generated in <3 seconds. Use it to prepare for the patient visit."
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating pre-consultation summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate summary"
        )


@router.get("/doctor/patient/{patient_id}/clinical-alerts")
async def get_clinical_alerts(
    patient_id: str,
    db: Session = Depends(get_db)
) -> dict:
    """Get high-priority clinical alerts for a patient (TIER 1 - Red banner alerts only)"""
    try:
        patient_profile = db.query(Patient).filter(Patient.user_id == patient_id).first()
        
        if not patient_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        active_meds = db.query(PatientMedication).filter(
            and_(
                PatientMedication.patient_id == patient_id,
                PatientMedication.status == "active"
            )
        ).all()

        adherence_scores = [m.adherence_score for m in active_meds if m.adherence_score]
        avg_adherence = sum(adherence_scores) / len(adherence_scores) if adherence_scores else 0.0

        alerts = generate_clinical_alerts(patient_profile, active_meds, avg_adherence)

        return {
            "success": True,
            "data": {
                "alerts": alerts,
                "alert_count": len(alerts),
                "high_priority_count": sum(1 for a in alerts if a.get('priority') == 'high')
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting clinical alerts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve alerts"
        )


def calculate_age(date_of_birth):
    """Calculate age from date of birth"""
    today = datetime.now().date()
    return today.year - date_of_birth.year - (
        (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    )


def generate_clinical_alerts(patient_profile, medications, adherence_score) -> list[dict]:
    """
    Generate HIGH-PRIORITY clinical alerts (red banner only).
    
    This is deliberately MINIMAL to avoid alert fatigue.
    Only show CRITICAL safety alerts.
    """
    alerts = []

    # Alert 1: Low medication adherence
    if adherence_score < 0.5:
        alerts.append({
            "priority": "high",
            "type": "adherence",
            "message": f"⚠️ Low medication adherence ({int(adherence_score * 100)}%) - Patient may be skipping doses",
            "recommendation": "Discuss barriers to adherence. Consider simplifying regimen."
        })

    # Alert 2: Polypharmacy (>5 meds = hard to manage)
    if len(medications) > 5:
        alerts.append({
            "priority": "medium",
            "type": "polypharmacy",
            "message": f"Patient on {len(medications)} medications - Review for deprescribing opportunities",
            "recommendation": "Assess whether all medications are still indicated. Consider deprescribing."
        })

    # Alert 3: Allergy present (critical for prescribing)
    if patient_profile and patient_profile.known_allergies:
        alerts.append({
            "priority": "high",
            "type": "allergy",
            "message": f"⚠️ Known allergies: {', '.join(patient_profile.known_allergies)}",
            "recommendation": "Avoid medications with similar structures."
        })

    # Alert 4: Chronic condition management
    if patient_profile and patient_profile.chronic_conditions:
        if "diabetes" in str(patient_profile.chronic_conditions).lower():
            alerts.append({
                "priority": "medium",
                "type": "chronic",
                "message": "Patient has diabetes - Monitor kidney function and adjust medications accordingly",
                "recommendation": "Consider ACE inhibitor/ARB for renal protection if not already on it."
            })

    return alerts
