"""
LLM Tools for Gemini Tool Calling

Each tool is independently callable by Gemini.
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from bloodflow_ai.schemas.donor_schema import Donor
from bloodflow_ai.schemas.request_schema import HospitalRequest
from bloodflow_ai.rag.rag_tool import RAGTool

class LLMTools:
    """Collection of tools that Gemini can call."""

    def ask_rag(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using RAG.
        Args:
            question: User question
        Returns:
            Dict with answer and sources
        """
        print(f"[Tool] ask_rag('{question[:50]}...')")
    
        # Initialize RAG tool if not already done
        if not hasattr(self, '_rag_tool'):
            self._rag_tool = RAGTool()
            self._rag_tool.load()
        
        return self._rag_tool.ask(question)
    
    def __init__(self, donor_store: Optional[List[Donor]] = None):
        """Initialize with optional donor data."""
        self.donors = donor_store or []
        self._contacted_this_run = []
    
    def find_nearest_donors(
        self,
        blood_group: str,
        location: str = "Dhaka",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find donors by blood group and location.
        
        Args:
            blood_group: Blood group to match (e.g., "O-")
            location: City to search (e.g., "Dhaka")
            limit: Maximum number to return
        
        Returns:
            List of donor dicts
        """
        print(f"[Tool] find_nearest_donors({blood_group}, {location})")
        
        compatible = []
        for donor in self.donors:
            if self._is_compatible(donor.blood_group, blood_group):
                compatible.append(donor)
        
        # Sort by location match
        compatible.sort(key=lambda d: 0 if d.location == location else 1)
        
        return [d.model_dump() for d in compatible[:limit]]
    
    def check_availability(self, donor_id: int) -> Dict[str, Any]:
        """
        Check if a donor is available and eligible.
        
        Args:
            donor_id: Donor ID to check
        
        Returns:
            Dict with available status and reason
        """
        print(f"[Tool] check_availability({donor_id})")
        
        donor = None
        for d in self.donors:
            if d.id == donor_id:
                donor = d
                break
        
        if not donor:
            return {"available": False, "reason": "Donor not found"}
        
        if not donor.available:
            return {"available": False, "reason": "Donor is not available"}
        
        if donor.status != "Active":
            return {"available": False, "reason": f"Donor status: {donor.status}"}
        
        if donor.last_donation:
            try:
                from datetime import datetime
                last_date = datetime.strptime(donor.last_donation, "%Y-%m-%d")
                days_since = (datetime.now() - last_date).days
                if days_since < 90:
                    return {"available": False, "reason": f"Cooldown: {90 - days_since} days remaining"}
            except (ValueError, TypeError):
                pass
        
        return {"available": True, "reason": "Donor is eligible"}
    
    def rank_donors(self, donors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank donors by score.
        
        Args:
            donors: List of donor dicts
        
        Returns:
            Ranked donor list with score
        """
        print(f"[Tool] rank_donors({len(donors)} donors)")
        
        scored = []
        for donor in donors:
            score = 0.0
            score += donor.get("response_rate", 0.5) * 0.4
            
            if donor.get("available", False):
                score += 0.3
            
            score += 0.1
            
            if donor.get("last_donation"):
                score += 0.1
            
            donor_copy = donor.copy()
            donor_copy["score"] = round(score, 2)
            scored.append(donor_copy)
        
        scored.sort(key=lambda x: x.get("score", 0), reverse=True)
        return scored
    
    def notify_donor(self, donor_id: int, message: str) -> Dict[str, Any]:
        """
        Notify a donor.
        
        Args:
            donor_id: Donor ID to notify
            message: Message to send
        
        Returns:
            Dict with notification status
        """
        print(f"[Tool] notify_donor({donor_id}, '{message[:30]}...')")
        
        donor = None
        for d in self.donors:
            if d.id == donor_id:
                donor = d
                break
        
        if not donor:
            return {"status": "failed", "reason": "Donor not found"}
        
        if donor.id in self._contacted_this_run:
            return {"status": "failed", "reason": "Donor already contacted"}
        
        self._contacted_this_run.append(donor.id)
        
        # Simulate acceptance based on response rate
        import random
        accepted = random.random() < donor.response_rate
        
        return {
            "status": "accepted" if accepted else "declined",
            "donor": donor.name,
            "message": f"Donor {donor.name} {'accepted' if accepted else 'declined'} the request"
        }
    
    def get_donor_details(self, donor_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a donor.
        
        Args:
            donor_id: Donor ID
        
        Returns:
            Donor dict
        """
        print(f"[Tool] get_donor_details({donor_id})")
        
        for d in self.donors:
            if d.id == donor_id:
                return d.model_dump()
        
        return {"error": "Donor not found"}
    
    def _is_compatible(self, donor_blood: str, patient_blood: str) -> bool:
        """Check blood group compatibility."""
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
