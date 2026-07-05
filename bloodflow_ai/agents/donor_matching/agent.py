"""
Donor Matching Agent

Ranks and filters donors based on compatibility with the hospital request.
"""

import csv
from pathlib import Path
from typing import List, Optional, Any

from bloodflow_ai.schemas.request_schema import HospitalRequest
from bloodflow_ai.schemas.donor_schema import Donor
from bloodflow_ai.tools.compatibility import CompatibilityChecker
from bloodflow_ai.tools.eligibility import EligibilityChecker


class DonorMatchingAgent:
    """
    Matches and ranks donors based on compatibility.
    
    Responsibilities:
    1. Filter donors by blood group compatibility
    2. Filter donors by eligibility (cooldown, age, etc.)
    3. Rank donors by distance, response rate, and availability
    4. Return top N donors
    
    Single Responsibility: Donor ranking only.
    """
    
    def __init__(self, donor_list: Optional[List[Donor]] = None):
        """
        Initialize the Matching Agent.
        
        Args:
            donor_list: Optional list of donors. If not provided, loads default from CSV.
        """
        self.compatibility = CompatibilityChecker()
        self.eligibility = EligibilityChecker()
        
        if donor_list:
            self.donors = donor_list
        else:
            self.donors = self._load_default_donors()
    
    def match(
        self,
        request: HospitalRequest,
        max_results: int = 5,
        context: Optional[Any] = None
    ) -> List[Donor]:
        """
        Find and rank the best donors for a given request.
        
        Args:
            request: Structured hospital request
            max_results: Maximum number of donors to return
            context: Optional workflow context for logging/timing
            
        Returns:
            List of ranked donor objects (best first)
        """
        print(f"[Matching] Processing request for {request.blood_group}")
        
        if context:
            context.log_event("Matching", "🔍 Processing request", f"Blood: {request.blood_group}")
        
        # Step 1: Filter by blood compatibility
        compatible = self.compatibility.filter_by_blood_group(
            self.donors, request.blood_group
        )
        print(f"[Matching] Found {len(compatible)} compatible donors")
        
        # Step 2: Filter by eligibility
        eligible = self.eligibility.filter_by_eligibility(compatible)
        print(f"[Matching] Found {len(eligible)} eligible donors")
        
        # Step 3: Rank donors
        ranked = self._rank_donors(eligible, request)
        print(f"[Matching] Ranked {len(ranked)} donors")
        
        # Step 4: Return top N
        return ranked[:max_results]
    
    def _rank_donors(
        self,
        donors: List[Donor],
        request: HospitalRequest
    ) -> List[Donor]:
        """
        Rank donors by score (higher is better).
        
        Scoring factors:
        1. Response rate (0-1) → max 0.4
        2. Availability (prefer available) → max 0.3
        3. Distance (prefer closer) → max 0.2
        4. Recent donation (prefer longer ago) → max 0.1
        """
        scored = []
        
        for donor in donors:
            score = 0.0
            
            # Factor 1: Response rate (max 0.4)
            score += donor.response_rate * 0.4
            
            # Factor 2: Availability (max 0.3)
            if donor.available:
                score += 0.3
            
            # Factor 3: Distance bonus (stub)
            score += 0.1
            
            # Factor 4: Cooldown bonus (max 0.2)
            if donor.last_donation:
                score += 0.1
            
            scored.append((donor, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [donor for donor, _ in scored]
    
    def _load_default_donors(self) -> List[Donor]:
        """
        Load donors from bloodflow_ai/data/donors.csv.
        
        Returns:
            List of Donor objects loaded from CSV
        """
        # ✅ CORRECT PATH: Go up to bloodflow_ai/ then into data/
        csv_path = Path(__file__).resolve().parents[2] / "data" / "donors.csv"
        
        print(f"[Matching] Looking for CSV at: {csv_path}")
        
        if not csv_path.exists():
            print(f"[Matching] ⚠️ Warning: {csv_path} not found. Using empty donor list.")
            return []
        
        donors = []
        
        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                expected_fields = [
                    'id', 'name', 'blood_group', 'age', 'location', 'phone',
                    'last_donation', 'available', 'response_rate', 'preferred_time', 'status'
                ]
                
                if reader.fieldnames and all(field in reader.fieldnames for field in expected_fields):
                    for row in reader:
                        try:
                            # Handle last_donation properly
                            last_donation = row['last_donation']
                            if last_donation == '' or last_donation is None:
                                last_donation = None
                            
                            donor = Donor(
                                id=int(row['id']),
                                name=row['name'],
                                blood_group=row['blood_group'],
                                age=int(row['age']),
                                location=row['location'],
                                phone=row['phone'],
                                last_donation=last_donation,
                                available=row['available'].lower() == 'true',
                                response_rate=float(row['response_rate']),
                                preferred_time=row['preferred_time'],
                                status=row['status']
                            )
                            donors.append(donor)
                        except (ValueError, KeyError) as e:
                            print(f"[Matching] ⚠️ Skipping invalid row: {row} - {e}")
                            continue
                else:
                    print(f"[Matching] ⚠️ CSV headers don't match expected schema.")
                    print(f"[Matching] Expected: {expected_fields}")
                    print(f"[Matching] Found: {reader.fieldnames}")
                    return []
                    
        except Exception as e:
            print(f"[Matching] ❌ Error loading CSV: {e}")
            return []
        
        print(f"[Matching] ✅ Loaded {len(donors)} donors from CSV")
        return donors