"""
Emergency Triage Agent

Transforms unstructured hospital blood requests into structured data.
Uses rule-based pattern matching (no LLM required).
"""

import re
from typing import Optional, List, Dict, Any

from bloodflow_ai.schemas.request_schema import HospitalRequest


class EmergencyTriageAgent:
    """
    Extracts structured data from free-text hospital blood requests.
    
    Responsibilities:
    1. Extract blood group (O-, A+, B-, etc.)
    2. Extract hospital name from known list
    3. Detect urgency level (Critical, High, Normal)
    4. Extract deadline/time information
    5. Extract number of units requested
    6. Return clean HospitalRequest object
    """
    
    # Blood group patterns (ordered: long patterns first, then short patterns)
    BLOOD_GROUP_PATTERNS: List[tuple] = [
        # Long forms (higher priority)
        (r'\bO\s*[-–—]?\s*[Nn]egative\b', 'O-'),
        (r'\bO\s*[-–—]?\s*[Pp]ositive\b', 'O+'),
        (r'\bA\s*[-–—]?\s*[Nn]egative\b', 'A-'),
        (r'\bA\s*[-–—]?\s*[Pp]ositive\b', 'A+'),
        (r'\bB\s*[-–—]?\s*[Nn]egative\b', 'B-'),
        (r'\bB\s*[-–—]?\s*[Pp]ositive\b', 'B+'),
        (r'\bAB\s*[-–—]?\s*[Nn]egative\b', 'AB-'),
        (r'\bAB\s*[-–—]?\s*[Pp]ositive\b', 'AB+'),
        # Short forms (lower priority - fallback)
        (r'\bO[-–—]?\b', 'O-'),
        (r'\bA[-–—]?\b', 'A+'),
        (r'\bB[-–—]?\b', 'B+'),
        (r'\bAB[-–—]?\b', 'AB+'),
    ]
    
    # Known hospital names (expand as needed)
    KNOWN_HOSPITALS: List[str] = [
        "Square Hospital",
        "Dhaka Medical College Hospital",
        "Apollo Hospital Dhaka",
        "Combined Military Hospital",
        "Evercare Hospital Dhaka",
        "United Hospital Dhaka",
        "Bangabandhu Sheikh Mujib Medical University",
        "Ibn Sina Hospital",
        "Popular Medical College Hospital",
        "Labaid Hospital",
        "Anwar Khan Modern Hospital",
        "Central Hospital",
        "National Institute of Cardiovascular Diseases",
        "Dhaka Shishu Hospital",
        "Kurmitola General Hospital",
    ]
    
    # Urgency keyword mapping
    URGENCY_KEYWORDS: Dict[str, List[str]] = {
        "Critical": [
            "urgent", "emergency", "immediate", "asap", "critical", 
            "stat", "life", "threatening", "code red",
            "need now", "right away"
        ],
        "High": [
            "soon", "quickly", "priority", "needed today", 
            "today", "within hours", "high priority"
        ],
        "Normal": [
            "routine", "scheduled", "normal", "standard"
        ]
    }
    
    # Time patterns for deadline extraction
    TIME_PATTERNS: List[str] = [
        r'before\s+(\d{1,2}\s*[AP]M)',
        r'by\s+(\d{1,2}\s*[AP]M)',
        r'(\d{1,2}\s*[AP]M)',
        r'within\s+(\d+)\s*hours?',
        r'(\d+)\s*hours?',
        r'\b(today|tomorrow|tonight|morning|afternoon|evening)\b'
    ]
    
    def __init__(self, hospital_list: Optional[List[str]] = None):
        """
        Initialize the Emergency Triage Agent.
        
        Args:
            hospital_list: Optional custom list of hospital names.
                          If not provided, uses default list.
        """
        if hospital_list:
            self.KNOWN_HOSPITALS = hospital_list
    
    def process(
        self,
        raw_text: str,
        context: Optional[Any] = None  # ← NEW: Accept context parameter
    ) -> Optional[HospitalRequest]:
        """
        Process raw text and return structured HospitalRequest.
        
        Args:
            raw_text: Unstructured request string from hospital
            context: Optional workflow context for logging/timing
            
        Returns:
            HospitalRequest object or None if text is invalid
        """
        if not raw_text or not raw_text.strip():
            if context:
                context.log_event("Emergency", "❌ Failed", "Empty input")
            return None
        
        # Clean the input
        text = raw_text.strip()
        
        # Log to context if provided
        if context:
            context.log_event("Emergency", "🔍 Parsing", text[:50] + "..." if len(text) > 50 else text)
        
        # Extract fields
        blood_group = self._extract_blood_group(text)
        hospital = self._extract_hospital(text)
        urgency = self._extract_urgency(text)
        deadline = self._extract_deadline(text)
        units = self._extract_units(text)
        
        # Create structured request
        return HospitalRequest(
            blood_group=blood_group or "Unknown",
            hospital=hospital or "Unknown Hospital",
            urgency=urgency or "Normal",
            deadline=deadline or "As soon as possible",
            units=units or 1,
            raw_input=text
        )
    
    def _extract_blood_group(self, text: str) -> Optional[str]:
        """Extract blood group from text using regex patterns."""
        for pattern, group in self.BLOOD_GROUP_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return group
        return None
    
    def _extract_hospital(self, text: str) -> Optional[str]:
        """Extract hospital name by matching against known hospitals."""
        sorted_hospitals = sorted(self.KNOWN_HOSPITALS, key=len, reverse=True)
        for hospital in sorted_hospitals:
            if hospital.lower() in text.lower():
                return hospital
        return None
    
    def _extract_urgency(self, text: str) -> Optional[str]:
        """Detect urgency level based on keyword presence."""
        text_lower = text.lower()
        
        for keyword in self.URGENCY_KEYWORDS["Critical"]:
            if keyword in text_lower:
                return "Critical"
        
        for keyword in self.URGENCY_KEYWORDS["High"]:
            if keyword in text_lower:
                return "High"
        
        return "Normal"
    
    def _extract_deadline(self, text: str) -> Optional[str]:
        """Extract deadline/time information from text."""
        for pattern in self.TIME_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if match.groups():
                    return match.group(1)
                else:
                    return match.group(0)
        return None
    
    def _extract_units(self, text: str) -> Optional[int]:
        """Extract number of blood units requested."""
        patterns = [
            r'(\d+)\s*units?',
            r'(\d+)\s*bags?',
            r'(\d+)\s*bag(s)?',
            r'(\d+)\s*unit(s)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
