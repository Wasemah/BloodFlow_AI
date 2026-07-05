"""
Decision Engine

Explains every decision made by the system.
Never changes decisions — only explains them.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from bloodflow_ai.schemas.donor_schema import Donor
from bloodflow_ai.schemas.request_schema import HospitalRequest
from bloodflow_ai.schemas.comm_schema import CommResult


class DecisionEngine:
    """
    Generates structured explanations for AI decisions.
    
    Answers:
    - Why this donor?
    - Why not another donor?
    - Why communication started?
    - Why retry happened?
    """
    
    def __init__(self):
        self._explanations: Dict[str, Dict[str, Any]] = {}
    
    def explain_donor_selection(
        self,
        selected_donor: Donor,
        all_donors: List[Donor],
        request: HospitalRequest,
        scores: Dict[int, float]
    ) -> Dict[str, Any]:
        """
        Explain why a specific donor was selected.
        
        Args:
            selected_donor: The donor who was selected
            all_donors: All donors considered
            request: The hospital request
            scores: Dictionary mapping donor_id to score
            
        Returns:
            Structured explanation
        """
        reasons = []
        
        # Reason 1: Blood match
        if selected_donor.blood_group == request.blood_group:
            reasons.append({
                "type": "blood_match",
                "description": f"Exact blood match: {selected_donor.blood_group}",
                "importance": "critical"
            })
        else:
            # Check if compatible (O- universal donor case)
            from bloodflow_ai.tools.compatibility import CompatibilityChecker
            checker = CompatibilityChecker()
            if checker.is_compatible(selected_donor.blood_group, request.blood_group):
                reasons.append({
                    "type": "blood_compatible",
                    "description": f"Compatible blood type: {selected_donor.blood_group} → {request.blood_group}",
                    "importance": "high"
                })
        
        # Reason 2: Availability
        if selected_donor.available:
            reasons.append({
                "type": "availability",
                "description": "Donor is currently available",
                "importance": "high"
            })
        
        # Reason 3: Cooldown
        if selected_donor.last_donation:
            from datetime import datetime
            try:
                last_date = datetime.strptime(selected_donor.last_donation, "%Y-%m-%d")
                days_since = (datetime.now() - last_date).days
                if days_since >= 90:
                    reasons.append({
                        "type": "cooldown",
                        "description": f"Cooldown expired ({days_since} days since last donation)",
                        "importance": "medium"
                    })
                else:
                    reasons.append({
                        "type": "cooldown",
                        "description": f"Cooldown period respected (last donation: {days_since} days ago)",
                        "importance": "medium"
                    })
            except:
                pass
        
        # Reason 4: Response rate
        if selected_donor.response_rate > 0.7:
            reasons.append({
                "type": "response_rate",
                "description": f"High historical response rate: {selected_donor.response_rate:.0%}",
                "importance": "high"
            })
        elif selected_donor.response_rate > 0.5:
            reasons.append({
                "type": "response_rate",
                "description": f"Good historical response rate: {selected_donor.response_rate:.0%}",
                "importance": "medium"
            })
        
        # Reason 5: Location
        reasons.append({
            "type": "location",
            "description": f"Located in {selected_donor.location}",
            "importance": "medium"
        })
        
        # Reason 6: Score (if available)
        score = scores.get(selected_donor.id, 0)
        if score > 0:
            # Explain relative to other donors
            other_scores = [s for did, s in scores.items() if did != selected_donor.id]
            if other_scores:
                max_other = max(other_scores) if other_scores else 0
                if score > max_other:
                    reasons.append({
                        "type": "highest_score",
                        "description": f"Highest overall score: {score:.1f} (next best: {max_other:.1f})",
                        "importance": "critical"
                    })
                else:
                    reasons.append({
                        "type": "score",
                        "description": f"Strong overall score: {score:.1f}",
                        "importance": "high"
                    })
        
        explanation = {
            "donor_id": selected_donor.id,
            "donor_name": selected_donor.name,
            "blood_group": selected_donor.blood_group,
            "reasons": reasons,
            "summary": self._generate_summary(reasons),
            "timestamp": datetime.now().isoformat()
        }
        
        self._explanations[selected_donor.id] = explanation
        return explanation
    
    def explain_communication_decision(
        self,
        comm_result: CommResult,
        donors: List[Donor]
    ) -> Dict[str, Any]:
        """
        Explain communication decisions.
        
        Args:
            comm_result: Communication result
            donors: List of donors attempted
            
        Returns:
            Explanation of communication decisions
        """
        explanation = {
            "status": comm_result.status,
            "attempts": comm_result.attempts,
            "accepted_donor": comm_result.accepted_donor,
            "declined_donors": comm_result.declined_donors,
            "reason": ""
        }
        
        if comm_result.status == "success":
            explanation["reason"] = f"Donor {comm_result.accepted_donor} accepted the request after {comm_result.attempts} attempt(s)"
        else:
            if comm_result.attempts == 0:
                explanation["reason"] = "No donors were available to contact"
            else:
                explanation["reason"] = f"All {comm_result.attempts} contacted donors declined or did not respond"
        
        # Add per-donor status if available
        donor_status = []
        for donor in donors[:comm_result.attempts]:
            status = "declined"
            if donor.name == comm_result.accepted_donor:
                status = "accepted"
            donor_status.append({
                "name": donor.name,
                "status": status
            })
        
        explanation["donor_status"] = donor_status
        return explanation
    
    def _generate_summary(self, reasons: List[Dict[str, Any]]) -> str:
        """Generate a one-sentence summary from reasons."""
        critical = [r for r in reasons if r.get("importance") == "critical"]
        high = [r for r in reasons if r.get("importance") == "high"]
        
        if critical:
            return f"Selected because: {', '.join(r['description'] for r in critical[:2])}"
        elif high:
            return f"Selected because: {', '.join(r['description'] for r in high[:2])}"
        else:
            return f"Selected based on {len(reasons)} positive factors"
    
    def get_explanation(self, donor_id: int) -> Optional[Dict[str, Any]]:
        """Get the explanation for a specific donor."""
        return self._explanations.get(donor_id)