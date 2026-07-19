"""
tests/test_critical_features.py - Tests for TIER 1 critical features
Based on CTO strategic critique
"""

import pytest
from app.services.drug_interaction_service import DrugInteractionService
from app.services.ocr_confidence_service import OCRConfidenceService, ConfidenceLevel


class TestDrugInteractionService:
    """Test drug interaction detection (TIER 1 PRIORITY)"""
    
    def test_severe_interaction_detected(self):
        """Test that severe interactions are detected"""
        service = DrugInteractionService(db=None)
        
        # Aspirin + Ibuprofen should be SEVERE
        interaction = service._lookup_interaction("aspirin", "ibuprofen")
        
        assert interaction is not None
        assert interaction['severity'] == 'severe'
        assert 'bleeding' in interaction['interaction_description'].lower()

    def test_moderate_interaction_detected(self):
        """Test that moderate interactions are detected"""
        service = DrugInteractionService(db=None)
        
        # Sertraline + Ibuprofen should be MODERATE
        interaction = service._lookup_interaction("sertraline", "ibuprofen")
        
        assert interaction is not None
        assert interaction['severity'] == 'moderate'

    def test_no_interaction_returns_none(self):
        """Test that non-interacting drugs return None"""
        service = DrugInteractionService(db=None)
        
        interaction = service._lookup_interaction("aspirin", "lisinopril")
        
        # These don't interact in our database
        assert interaction is None

    def test_bidirectional_lookup(self):
        """Test that drug interactions work in both directions"""
        service = DrugInteractionService(db=None)
        
        interaction1 = service._lookup_interaction("aspirin", "ibuprofen")
        interaction2 = service._lookup_interaction("ibuprofen", "aspirin")
        
        assert interaction1 is not None
        assert interaction2 is not None
        assert interaction1['severity'] == interaction2['severity']


class TestOCRConfidenceService:
    """Test OCR confidence tracking (CTO CRITIQUE: Show confidence scores)"""
    
    def test_confidence_classification(self):
        """Test confidence level classification"""
        assert OCRConfidenceService.classify_confidence(0.98) == ConfidenceLevel.VERY_HIGH
        assert OCRConfidenceService.classify_confidence(0.90) == ConfidenceLevel.HIGH
        assert OCRConfidenceService.classify_confidence(0.75) == ConfidenceLevel.MEDIUM
        assert OCRConfidenceService.classify_confidence(0.65) == ConfidenceLevel.LOW
        assert OCRConfidenceService.classify_confidence(0.55) == ConfidenceLevel.VERY_LOW

    def test_should_auto_add_medication_name(self):
        """Test that medication names require very high confidence"""
        # Should auto-add at 95%
        assert OCRConfidenceService.should_auto_add('medication_name', 0.95) is True
        
        # Should NOT auto-add at 85%
        assert OCRConfidenceService.should_auto_add('medication_name', 0.85) is False

    def test_should_auto_add_diagnosis(self):
        """Test that diagnoses have lower threshold"""
        # Should auto-add at 82%
        assert OCRConfidenceService.should_auto_add('diagnosis', 0.82) is True
        
        # Should NOT auto-add at 75%
        assert OCRConfidenceService.should_auto_add('diagnosis', 0.75) is False

    def test_user_action_very_high_confidence(self):
        """Test action when confidence is very high"""
        action = OCRConfidenceService.get_user_action(
            'medication_name',
            0.98,
            'Lisinopril'
        )
        
        assert action['action'] == 'auto_add'
        assert not action['requires_action']

    def test_user_action_low_confidence(self):
        """Test action when confidence is low"""
        action = OCRConfidenceService.get_user_action(
            'medication_name',
            0.65,
            'Lisinopril'
        )
        
        assert action['action'] == 'review'
        assert action['requires_action']
        assert '⚠️' in action['message'] or '🔍' in action['message']

    def test_extraction_report_generation(self):
        """Test generation of extraction quality report"""
        extractions = [
            {'field_type': 'medication_name', 'confidence': 0.98, 'value': 'Lisinopril'},
            {'field_type': 'dosage', 'confidence': 0.92, 'value': '10mg'},
            {'field_type': 'diagnosis', 'confidence': 0.72, 'value': 'Hypertension'},
        ]
        
        report = OCRConfidenceService.generate_extraction_report(extractions)
        
        assert report['total_extracted'] == 3
        assert len(report['by_confidence']['very_high']) == 1
        assert len(report['by_confidence']['high']) == 1
        assert len(report['by_confidence']['medium']) == 1
        assert report['auto_add_count'] >= 1

    def test_quality_message_excellent(self):
        """Test quality message for excellent extraction"""
        message = OCRConfidenceService.get_quality_message(0.96)
        assert '✓' in message
        assert 'auto-added' in message.lower()

    def test_quality_message_poor(self):
        """Test quality message for poor extraction"""
        message = OCRConfidenceService.get_quality_message(0.55)
        assert '✗' in message or '🔍' in message


class TestCriticalFeatureIntegration:
    """Integration tests for TIER 1 features"""
    
    def test_upload_flow_with_confidence_check(self):
        """Test complete upload flow with confidence validation"""
        # Simulate extracted data from OCR
        extracted_data = {
            'medications': [
                {'name': 'Lisinopril', 'confidence': 0.97},
                {'name': 'Metformin', 'confidence': 0.82},
            ]
        }
        
        # Should auto-add high-confidence medication
        lisinopril_action = OCRConfidenceService.get_user_action(
            'medication_name', 0.97, 'Lisinopril'
        )
        assert lisinopril_action['action'] == 'auto_add'
        
        # Should require review for medium-confidence medication
        metformin_action = OCRConfidenceService.get_user_action(
            'medication_name', 0.82, 'Metformin'
        )
        assert metformin_action['action'] == 'confirm'

    def test_drug_conflict_alert_flow(self):
        """Test end-to-end drug conflict alert"""
        service = DrugInteractionService(db=None)
        
        # Lookup interaction
        interaction = service._lookup_interaction("warfarin", "aspirin")
        
        assert interaction is not None
        assert interaction['severity'] == 'severe'
        
        # Should show urgent alert
        action_info = OCRConfidenceService.get_user_action(
            'medication_name', 0.95, 'Aspirin'
        )
        
        # Create alert response (would be sent to frontend)
        alert = {
            'type': 'drug_interaction',
            'severity': 'severe',
            'message': f"SEVERE: {interaction['interaction_description']}",
            'recommendation': interaction['management_strategy'],
            'urgent': True
        }
        
        assert alert['urgent'] is True
        assert alert['severity'] == 'severe'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
