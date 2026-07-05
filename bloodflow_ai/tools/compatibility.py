"""
Blood Compatibility Checker

Pure functions for blood group compatibility.
"""

from typing import List
from bloodflow_ai.schemas.donor_schema import Donor


class CompatibilityChecker:
    """Handles blood group compatibility logic."""
    
    # Universal compatibility rules
    # Key: recipient blood group, Value: list of compatible donor blood groups
    COMPATIBILITY_MAP = {
        "O-": ["O-"],
        "O+": ["O-", "O+"],
        "A-": ["O-", "A-"],
        "A+": ["O-", "O+", "A-", "A+"],
        "B-": ["O-", "B-"],
        "B+": ["O-", "O+", "B-", "B+"],
        "AB-": ["O-", "A-", "B-", "AB-"],
        "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    }
    
    def is_compatible(self, donor_blood: str, patient_blood: str) -> bool:
        """
        Check if donor blood is compatible with patient blood.
        
        Args:
            donor_blood: Donor's blood group (e.g., "O-")
            patient_blood: Patient's blood group (e.g., "A+")
            
        Returns:
            True if compatible, False otherwise
        """
        compatible_types = self.COMPATIBILITY_MAP.get(patient_blood, [])
        return donor_blood in compatible_types
    
    def filter_by_blood_group(
        self,
        donors: List[Donor],
        patient_blood: str
    ) -> List[Donor]:
        """
        Filter donors by blood group compatibility.
        
        Args:
            donors: List of donor objects
            patient_blood: Patient's blood group
            
        Returns:
            List of compatible donors
        """
        return [
            donor for donor in donors
            if self.is_compatible(donor.blood_group, patient_blood)
        ]
