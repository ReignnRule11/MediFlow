"""
app/services/ocr_confidence_service.py - OCR confidence tracking and validation
CTO CRITIQUE: Flag low-confidence extractions for review
"""

from enum import Enum
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ConfidenceLevel(str, Enum):
    """OCR confidence categorization"""
    VERY_HIGH = "very_high"      # 95-100%: Auto-process
    HIGH = "high"                # 85-94%: Auto-process with flag
    MEDIUM = "medium"            # 70-84%: Suggest review
    LOW = "low"                  # 60-69%: Require manual review
    VERY_LOW = "very_low"        # <60%: Reject, retry


class OCRConfidenceService:
    """
    Tracks OCR confidence and prevents low-confidence data from being used.
    
    TIER 1 PRIORITY: Only high-confidence extractions should auto-add to timeline.
    Low-confidence should be flagged for patient review.
    """

    # Confidence thresholds per field type
    FIELD_THRESHOLDS = {
        'medication_name': 0.90,      # Very strict - wrong drug = harm
        'dosage': 0.85,               # Strict - wrong dose = harm  
        'frequency': 0.80,            # Moderate - less critical
        'lab_value': 0.90,            # Strict - wrong lab = bad clinical decision
        'appointment_date': 0.85,     # Moderate-strict - affects scheduling
        'diagnosis': 0.80,            # Moderate - informational
    }

    @staticmethod
    def classify_confidence(score: float) -> ConfidenceLevel:
        """Classify confidence score into levels"""
        if score >= 0.95:
            return ConfidenceLevel.VERY_HIGH
        elif score >= 0.85:
            return ConfidenceLevel.HIGH
        elif score >= 0.70:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.60:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

    @staticmethod
    def should_auto_add(field_type: str, confidence: float) -> bool:
        """Determine if extracted data should be auto-added to patient profile"""
        threshold = OCRConfidenceService.FIELD_THRESHOLDS.get(field_type, 0.80)
        return confidence >= threshold

    @staticmethod
    def get_user_action(
        field_type: str,
        confidence: float,
        extracted_value: str
    ) -> Dict[str, any]:
        """
        Determine what action to show to patient.
        
        Returns:
            {
                'action': 'auto_add' | 'confirm' | 'review' | 'reject',
                'message': str,
                'suggested_value': str,
                'requires_action': bool
            }
        """
        confidence_level = OCRConfidenceService.classify_confidence(confidence)
        should_auto = OCRConfidenceService.should_auto_add(field_type, confidence)

        if confidence_level == ConfidenceLevel.VERY_HIGH:
            return {
                'action': 'auto_add',
                'message': f'✓ Automatically added (confidence: {int(confidence*100)}%)',
                'suggested_value': extracted_value,
                'requires_action': False
            }

        elif confidence_level == ConfidenceLevel.HIGH:
            return {
                'action': 'confirm',
                'message': f'⚠️ Confidence: {int(confidence*100)}% - Please review',
                'suggested_value': extracted_value,
                'requires_action': True,
                'cta': 'Confirm to add to timeline'
            }

        elif confidence_level == ConfidenceLevel.MEDIUM:
            return {
                'action': 'review',
                'message': f'⚠️ Low confidence: {int(confidence*100)}% - Please verify this is correct:',
                'suggested_value': extracted_value,
                'requires_action': True,
                'cta': 'Review & confirm'
            }

        elif confidence_level == ConfidenceLevel.LOW:
            return {
                'action': 'review',
                'message': f'🔍 Very low confidence: {int(confidence*100)}% - This may be incorrect',
                'suggested_value': extracted_value,
                'requires_action': True,
                'cta': 'Manual review required'
            }

        else:  # VERY_LOW
            return {
                'action': 'reject',
                'message': f'✗ Confidence too low ({int(confidence*100)}%) - Cannot be used',
                'suggested_value': None,
                'requires_action': True,
                'cta': 'Re-upload or enter manually'
            }

    @staticmethod
    def generate_extraction_report(extractions: List[Dict]) -> Dict:
        """
        Generate a report on extraction quality and recommended actions.
        
        Used in upload flow to show patient what was extracted and what needs review.
        """
        report = {
            'total_extracted': len(extractions),
            'by_confidence': {
                'very_high': [],
                'high': [],
                'medium': [],
                'low': [],
                'very_low': []
            },
            'requires_review': [],
            'cannot_use': [],
            'auto_add_count': 0,
            'quality_score': 0.0  # Average confidence
        }

        confidence_scores = []

        for extraction in extractions:
            field_type = extraction.get('field_type', 'unknown')
            confidence = extraction.get('confidence', 0.0)
            value = extraction.get('value')

            confidence_scores.append(confidence)
            level = OCRConfidenceService.classify_confidence(confidence)

            item = {
                'field': field_type,
                'value': value,
                'confidence': int(confidence * 100)
            }

            report['by_confidence'][level.value].append(item)

            action_info = OCRConfidenceService.get_user_action(field_type, confidence, value)

            if action_info['action'] == 'auto_add':
                report['auto_add_count'] += 1
            elif action_info['action'] in ['review', 'confirm']:
                report['requires_review'].append(item)
            elif action_info['action'] == 'reject':
                report['cannot_use'].append(item)

        report['quality_score'] = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.0
        )

        return report

    @staticmethod
    def get_quality_message(quality_score: float) -> str:
        """Generate user-friendly quality message"""
        if quality_score >= 0.95:
            return "✓ Excellent extraction quality - data auto-added"
        elif quality_score >= 0.85:
            return "✓ Good extraction quality - please review flagged items"
        elif quality_score >= 0.70:
            return "⚠️ Fair extraction quality - please review carefully"
        elif quality_score >= 0.60:
            return "🔍 Low extraction quality - manual review required"
        else:
            return "✗ Poor extraction quality - re-upload or enter manually"
