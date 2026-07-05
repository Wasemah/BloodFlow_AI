"""
Score Breakdown

Exposes how donor scores were calculated.
"""

from typing import Dict, Any, List
from bloodflow_ai.schemas.donor_schema import Donor


class ScoreBreakdown:
    """
    Produces detailed score breakdowns for donors.
    
    Instead of: Score = 96
    Shows: Blood Match = 40, Availability = 20, Distance = 18, Response Rate = 12, Cooldown = 6
    """
    
    def __init__(self):
        self._breakdowns: Dict[int, Dict[str, Any]] = {}
    
    def breakdown(self, donor: Donor, score: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produce a detailed score breakdown.
        
        Args:
            donor: The donor to breakdown
            score: The total score
            context: Additional context (request, distances, etc.)
            
        Returns:
            Detailed score breakdown
        """
        components = {}
        
        # Component 1: Blood compatibility (max 40)
        blood_score = self._calculate_blood_score(donor, context)
        components["Blood Compatibility"] = blood_score
        
        # Component 2: Availability (max 20)
        availability_score = 20 if donor.available else 0
        components["Availability"] = availability_score
        
        # Component 3: Distance (max 18)
        distance_score = self._calculate_distance_score(donor, context)
        components["Distance"] = distance_score
        
        # Component 4: Response Rate (max 12)
        response_score = donor.response_rate * 12
        components["Response Rate"] = round(response_score, 1)
        
        # Component 5: Cooldown (max 10)
        cooldown_score = self._calculate_cooldown_score(donor)
        components["Cooldown"] = cooldown_score
        
        # Calculate total
        total = sum(components.values())
        
        breakdown = {
            "donor_id": donor.id,
            "donor_name": donor.name,
            "components": components,
            "total": round(total, 1),
            "score": score,
            "timestamp": context.get("timestamp", "")
        }
        
        self._breakdowns[donor.id] = breakdown
        return breakdown
    
    def _calculate_blood_score(self, donor: Donor, context: Dict[str, Any]) -> float:
        """Calculate blood compatibility score (max 40)."""
        request_blood = context.get("blood_group", "")
        
        if donor.blood_group == request_blood:
            return 40.0
        elif self._is_compatible(donor.blood_group, request_blood):
            return 30.0
        else:
            return 0.0
    
    def _calculate_distance_score(self, donor: Donor, context: Dict[str, Any]) -> float:
        """Calculate distance score (max 18)."""
        # This is a stub — in production, calculate actual distance
        # For now, use a random score based on location
        distances = {"Dhaka": 0, "Chittagong": 10, "Rajshahi": 20, "Khulna": 15}
        base_distance = distances.get(donor.location, 25)
        
        # Score inversely proportional to distance
        if base_distance <= 5:
            return 18.0
        elif base_distance <= 10:
            return 14.0
        elif base_distance <= 15:
            return 10.0
        elif base_distance <= 20:
            return 6.0
        else:
            return 2.0
    
    def _calculate_cooldown_score(self, donor: Donor) -> float:
        """Calculate cooldown score (max 10)."""
        if not donor.last_donation:
            return 10.0
        
        from datetime import datetime
        try:
            last_date = datetime.strptime(donor.last_donation, "%Y-%m-%d")
            days_since = (datetime.now() - last_date).days
            
            if days_since >= 180:
                return 10.0
            elif days_since >= 90:
                return 6.0
            else:
                return 2.0
        except:
            return 5.0
    
    def _is_compatible(self, donor_blood: str, patient_blood: str) -> bool:
        """Check blood compatibility."""
        compatibility_map = {
            "O-": ["O-"],
            "O+": ["O-", "O+"],
            "A-": ["O-", "A-"],
            "A+": ["O-", "O+", "A-", "A+"],
            "B-": ["O-", "B-"],
            "B+": ["O-", "O+", "B-", "B+"],
            "AB-": ["O-", "A-", "B-", "AB-"],
            "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        }
        compatible = compatibility_map.get(patient_blood, [])
        return donor_blood in compatible
    
    def get_breakdown(self, donor_id: int) -> Dict[str, Any]:
        """Get the breakdown for a specific donor."""
        return self._breakdowns.get(donor_id, {})