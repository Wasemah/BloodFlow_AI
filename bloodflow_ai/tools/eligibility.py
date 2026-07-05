"""
Eligibility Checker

Pure functions for donor eligibility checking.
"""

from typing import List
from datetime import datetime
from bloodflow_ai.schemas.donor_schema import Donor


class EligibilityChecker:
    """Handles donor eligibility logic."""
    
    MIN_AGE = 18
    MAX_AGE = 65
    MIN_COOLDOWN_DAYS = 90
    
    def is_eligible(self, donor: Donor) -> bool:
        """
        Check if a donor is eligible to donate.
        
        Criteria:
        1. Age between 18-65
        2. Available flag is True
        3. No donation in last 90 days
        4. Status is "Active"
        """
        if not (self.MIN_AGE <= donor.age <= self.MAX_AGE):
            return False
        
        if not donor.available:
            return False
        
        if donor.status != "Active":
            return False
        
        if not self._cooldown_passed(donor):
            return False
        
        return True
    
    def _cooldown_passed(self, donor: Donor) -> bool:
        """Check if donor's cooldown period has passed."""
        if not donor.last_donation:
            return True
        
        try:
            last_date = None
            if isinstance(donor.last_donation, str):
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]:
                    try:
                        last_date = datetime.strptime(donor.last_donation, fmt)
                        break
                    except ValueError:
                        continue
                
                if last_date is None:
                    return True  # Assume eligible if date can't be parsed
            
            elif isinstance(donor.last_donation, datetime):
                last_date = donor.last_donation
            else:
                return True
            
            if last_date:
                days_since = (datetime.now() - last_date).days
                return days_since >= self.MIN_COOLDOWN_DAYS
                
        except Exception:
            return True  # Assume eligible on error
        
        return True
    
    def filter_by_eligibility(self, donors: List[Donor]) -> List[Donor]:
        """Filter donors by all eligibility criteria."""
        return [donor for donor in donors if self.is_eligible(donor)]
