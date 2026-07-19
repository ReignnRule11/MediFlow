"""
app/routers/drug_interactions.py - Real-time drug conflict detection endpoints
TIER 1 PRIORITY: Critical safety feature
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.services.drug_interaction_service import DrugInteractionService
from app.models import User
from app.dependencies import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/drug-interactions", tags=["drug-interactions"])


@router.get("/check")
async def check_medication_interaction(
    patient_id: str = Query(..., description="Patient ID"),
    new_medication_name: str = Query(..., description="New medication name to check"),
    db: Session = Depends(get_db)
) -> dict:
    """
    TIER 1: Check if new medication interacts with patient's current medications.
    
    This is the HIGHEST PRIORITY safety feature - prevents drug errors that cause ER visits.
    
    Returns only MODERATE and SEVERE interactions to avoid alert fatigue.
    """
    try:
        # Verify patient exists
        patient = db.query(User).filter(User.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        # Check interactions
        interaction_service = DrugInteractionService(db)
        interactions = interaction_service.check_interactions_for_new_medication(
            patient_id,
            new_medication_name
        )

        # Categorize by severity
        severe_interactions = [i for i in interactions if i['severity'] == 'severe']
        moderate_interactions = [i for i in interactions if i['severity'] == 'moderate']

        return {
            "success": True,
            "data": {
                "new_medication": new_medication_name,
                "has_interactions": len(interactions) > 0,
                "severe_interactions": severe_interactions,
                "moderate_interactions": moderate_interactions,
                "total_interactions": len(interactions),
                "recommendation": (
                    "DO NOT TAKE - Contact doctor immediately" if severe_interactions
                    else "Monitor closely - Discuss with doctor" if moderate_interactions
                    else "No known interactions"
                ),
                "urgent": bool(severe_interactions)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking interactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not check medication interactions"
        )


@router.get("/patient/{patient_id}/all")
async def get_all_patient_interactions(
    patient_id: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Get ALL interactions between patient's current medications.
    
    This is a comprehensive check of the patient's entire medication profile.
    Useful for periodic safety review.
    """
    try:
        patient = db.query(User).filter(User.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        interaction_service = DrugInteractionService(db)
        interactions = interaction_service.get_all_patient_interactions(patient_id)

        severe = [i for i in interactions if i['severity'] == 'severe']
        moderate = [i for i in interactions if i['severity'] == 'moderate']

        return {
            "success": True,
            "data": {
                "severe_interactions": severe,
                "moderate_interactions": moderate,
                "total_interactions": len(interactions),
                "risk_level": (
                    "HIGH - Multiple severe interactions" if len(severe) > 1
                    else "CRITICAL - Severe interaction found" if len(severe) == 1
                    else "MODERATE - Review cautiously" if len(moderate) > 0
                    else "LOW - No known interactions"
                )
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting all interactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve interactions"
        )
