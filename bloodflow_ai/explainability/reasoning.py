"""
Reasoning Generator

Converts structured decisions into natural language.
"""

from typing import Dict, Any, List, Optional
from bloodflow_ai.schemas.donor_schema import Donor


class ReasoningGenerator:
    """
    Generates human-readable reasoning from technical data.
    
    Example:
    "Rahim was selected because he has an exact blood match,
    has not donated recently, has the highest response probability,
    and lives closest to the hospital."
    """
    
    def __init__(self):
        self._reasonings: Dict[str, str] = {}
    
    def generate_selection_reasoning(
        self,
        donor: Donor,
        explanation: Dict[str, Any],
        breakdown: Dict[str, Any]
    ) -> str:
        """
        Generate natural language reasoning for donor selection.
        
        Args:
            donor: The selected donor
            explanation: DecisionEngine explanation
            breakdown: ScoreBreakdown breakdown
            
        Returns:
            Natural language explanation
        """
        parts = []
        
        # Start with name
        parts.append(f"{donor.name} was selected")
        
        # Add blood match reason
        reasons = explanation.get("reasons", [])
        blood_match = next((r for r in reasons if r["type"] in ["blood_match", "blood_compatible"]), None)
        if blood_match:
            parts.append("because they have a compatible blood type")
        else:
            # Use general blood group info
            parts.append(f"because they are blood type {donor.blood_group}")
        
        # Add availability
        if donor.available:
            parts.append("and are currently available to donate")
        
        # Add response rate
        if donor.response_rate > 0.7:
            parts.append(f"with a high historical response rate of {donor.response_rate:.0%}")
        elif donor.response_rate > 0.5:
            parts.append(f"with a response rate of {donor.response_rate:.0%}")
        
        # Add location
        if donor.location:
            parts.append(f"and are located in {donor.location}")
        
        # Add cooldown
        if donor.last_donation:
            from datetime import datetime
            try:
                last_date = datetime.strptime(donor.last_donation, "%Y-%m-%d")
                days_since = (datetime.now() - last_date).days
                if days_since >= 90:
                    parts.append(f"with {days_since} days since their last donation")
            except:
                pass
        
        # Add score context
        components = breakdown.get("components", {})
        if components:
            top_component = max(components.items(), key=lambda x: x[1])
            if top_component[1] > 0:
                parts.append(f"scoring highest in {top_component[0]} ({top_component[1]:.1f} points)")
        
        # Build final sentence
        reasoning = self._build_sentence(parts)
        self._reasonings[str(donor.id)] = reasoning
        return reasoning
    
    def generate_workflow_reasoning(
        self,
        request: Dict[str, Any],
        donor_name: Optional[str],
        status: str,
        duration: float
    ) -> str:
        """
        Generate reasoning for the overall workflow.
        
        Args:
            request: The hospital request
            donor_name: Name of selected donor
            status: Workflow status
            duration: Workflow duration
            
        Returns:
            Natural language workflow description
        """
        blood_group = request.get("blood_group", "unknown")
        hospital = request.get("hospital", "unknown hospital")
        
        if status == "success" and donor_name:
            return (
                f"The system successfully processed an emergency request for {blood_group} blood "
                f"at {hospital}. After analyzing potential donors, {donor_name} was selected "
                f"as the best match and successfully contacted. The entire workflow completed "
                f"in {duration:.2f} seconds."
            )
        elif status == "failed":
            return (
                f"The system processed an emergency request for {blood_group} blood at {hospital}. "
                f"However, no eligible donor accepted the request. The workflow completed "
                f"in {duration:.2f} seconds."
            )
        else:
            return (
                f"The system processed an emergency request for {blood_group} blood at {hospital} "
                f"in {duration:.2f} seconds."
            )
    
    def _build_sentence(self, parts: List[str]) -> str:
        """Build a grammatically correct sentence from parts."""
        if not parts:
            return "No reasoning available."
        
        # Remove duplicates
        seen = set()
        unique_parts = []
        for p in parts:
            if p not in seen:
                seen.add(p)
                unique_parts.append(p)
        
        # Join with proper punctuation
        if len(unique_parts) == 1:
            return unique_parts[0] + "."
        
        # Use commas and "and" for the last item
        *first, last = unique_parts
        return ", ".join(first) + ", and " + last + "."
    
    def get_reasoning(self, donor_id: int) -> Optional[str]:
        """Get the reasoning for a specific donor."""
        return self._reasonings.get(str(donor_id))