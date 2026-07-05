"""
Unit tests for Emergency Triage Agent.
"""

# pyrefly: ignore [missing-import]
import pytest
from bloodflow_ai.agents.emergency_triage.agent import EmergencyTriageAgent
from bloodflow_ai.schemas.request_schema import HospitalRequest


class TestEmergencyTriageAgent:
    """Test suite for EmergencyTriageAgent."""
    
    def setup_method(self):
        """Set up test fixture."""
        self.agent = EmergencyTriageAgent()
    
    def test_simple_request(self):
        """Test basic request with all fields present."""
        raw = "Need O- blood at Square Hospital before 8 PM"
        result = self.agent.process(raw)
        
        assert result is not None
        assert result.blood_group == "O-"
        assert result.hospital == "Square Hospital"
        assert result.urgency == "Normal"  # No urgency keywords
        assert result.deadline == "8 PM"
        assert result.units == 1
        assert result.raw_input == raw
    
    def test_urgent_request(self):
        """Test request with urgency keyword."""
        raw = "URGENT: A+ required for Dhaka Medical, 2 units needed"
        result = self.agent.process(raw)
        
        assert result is not None
        assert result.blood_group == "A+"
        assert result.hospital == "Dhaka Medical College Hospital"
        assert result.urgency == "Critical"
        assert result.units == 2
    
    def test_request_with_units(self):
        """Test request specifying number of units."""
        raw = "O+ blood needed immediately at Apollo Hospital, 3 units"
        result = self.agent.process(raw)
        
        assert result is not None
        assert result.blood_group == "O+"
        assert result.hospital == "Apollo Hospital Dhaka"
        assert result.urgency == "Critical"
        assert result.units == 3
    
    def test_minimal_request(self):
        """Test minimal request with only blood group and hospital."""
        raw = "Need B- at Combined Military Hospital"
        result = self.agent.process(raw)
        
        assert result is not None
        assert result.blood_group == "B-"
        assert result.hospital == "Combined Military Hospital"
        assert result.urgency == "Normal"
        assert result.deadline == "As soon as possible"
        assert result.units == 1
    
    def test_short_request(self):
        """Test short request (should return None)."""
        raw = "Need blood"
        result = self.agent.process(raw)
        assert result is None
    
    def test_empty_input(self):
        """Test empty input (should return None)."""
        result = self.agent.process("")
        assert result is None
        
        result = self.agent.process("   ")
        assert result is None
    
    def test_blood_group_variations(self):
        """Test various blood group formats."""
        test_cases = [
            ("O negative", "O-"),
            ("O positive", "O+"),
            ("A negative", "A-"),
            ("A positive", "A+"),
            ("AB positive", "AB+"),
            ("AB negative", "AB-"),
        ]
        
        for raw, expected in test_cases:
            request_text = f"Need {raw} blood at Hospital"
            result = self.agent.process(request_text)
            assert result is not None, f"Failed for: {raw}"
            assert result.blood_group == expected, f"Failed for: {raw}"
    
    def test_urgency_detection(self):
        """Test urgency detection for various keywords."""
        test_cases = [
            ("emergency", "Critical"),
            ("URGENT", "Critical"),
            ("asap", "Critical"),
            ("stat", "Critical"),
            ("soon", "High"),
            ("priority", "High"),
            ("today", "High"),
            ("routine", "Normal"),
            ("scheduled", "Normal"),
        ]
        
        for keyword, expected in test_cases:
            raw = f"Need O- at Hospital, this is {keyword}"
            result = self.agent.process(raw)
            assert result is not None, f"Failed for: {keyword}"
            assert result.urgency == expected, f"Failed for: {keyword}"
    
    def test_hospital_extraction(self):
        """Test hospital name extraction."""
        raw = "Need O- at Apollo Hospital Dhaka"
        result = self.agent.process(raw)
        assert result is not None
        assert result.hospital == "Apollo Hospital Dhaka"
    
    def test_deadline_extraction(self):
        """Test deadline/time extraction."""
        test_cases = [
            ("before 6 PM", "6 PM"),
            ("by 9 AM", "9 AM"),
            ("within 2 hours", "2"),
            ("need it today", "today"),
            ("by tomorrow", "tomorrow"),
        ]
        
        for text_suffix, expected in test_cases:
            raw = f"Need O- at Hospital {text_suffix}"
            result = self.agent.process(raw)
            assert result is not None, f"Failed for: {text_suffix}"
            assert result.deadline is not None, f"Failed for: {text_suffix}"
            assert expected in result.deadline, f"Failed for: {text_suffix}"
    
    def test_missing_blood_group(self):
        """Test request without blood group."""
        raw = "Need blood at Square Hospital"
        result = self.agent.process(raw)
        assert result is not None
        assert result.blood_group == "Unknown"
    
    def test_missing_hospital(self):
        """Test request without hospital name."""
        raw = "Need O- blood urgently"
        result = self.agent.process(raw)
        assert result is not None
        assert result.hospital == "Unknown Hospital"
    
    def test_known_hospitals_list(self):
        """Test that all known hospitals are recognized."""
        for hospital in self.agent.KNOWN_HOSPITALS:
            raw = f"Need O- at {hospital}"
            result = self.agent.process(raw)
            assert result is not None, f"Failed for: {hospital}"
            assert result.hospital == hospital, f"Failed for: {hospital}"
