"""
Communication Agent

Coordinates donor communication by iterating through ranked donors
until one accepts or all decline.
"""

import time
import random
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from bloodflow_ai.schemas.donor_schema import Donor
from bloodflow_ai.schemas.request_schema import HospitalRequest
from bloodflow_ai.schemas.comm_schema import CommResult
from bloodflow_ai.schemas.memory_schema import DonorMemory
from bloodflow_ai.memory.store import MemoryStore, InMemoryStore


class CommunicationAgent:
    """
    Autonomous communication coordinator.
    
    Responsibilities:
    1. Receive ranked donors list
    2. Iterate through donors in order
    3. Simulate contacting each donor (will be replaced with real APIs)
    4. Handle acceptance/decline/no-response
    5. Stop when a donor accepts or all decline
    6. Return structured CommResult
    
    Memory Integration:
    - Queries MemoryStore before contacting each donor
    - Skips donors in cooldown or already accepted
    - Stores interaction results for future use
    """
    
    def __init__(
        self,
        memory_store: Optional[MemoryStore] = None,
        cooldown_seconds: int = 3600,
        max_donors_to_try: int = 5
    ):
        """
        Initialize the Communication Agent.
        
        Args:
            memory_store: Optional memory store. Creates InMemoryStore if not provided.
            cooldown_seconds: Seconds to wait before contacting same donor again.
            max_donors_to_try: Maximum number of donors to iterate through.
        """
        self.memory_store = memory_store or InMemoryStore()
        self.cooldown_seconds = cooldown_seconds
        self.max_donors_to_try = max_donors_to_try
        self.contacted_this_session = []
        self.workflow_id = None
    
    def notify(
        self,
        request: HospitalRequest,
        donors: List[Donor],
        workflow_id: Optional[str] = None,
        context: Optional[Any] = None
    ) -> CommResult:
        """
        Coordinate donor communication.
        
        Args:
            request: The hospital request
            donors: Ranked list of donors (best first)
            workflow_id: Optional workflow ID for memory tracking
            context: Optional workflow context for logging/timing
            
        Returns:
            CommResult with status and details
        """
        start_time = time.time()
        self.workflow_id = workflow_id or f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Log to context if provided
        if context:
            context.log_event("Communication", "📞 STARTING", f"Donors: {len(donors)}, Workflow: {self.workflow_id}")
        
        print(f"\n[Communication] 📞 Starting coordination...")
        print(f"[Communication] Workflow ID: {self.workflow_id}")
        print(f"[Communication] Request: {request.blood_group} @ {request.hospital}")
        print(f"[Communication] Available donors: {len(donors)}")
        
        if not donors:
            if context:
                context.log_event("Communication", "❌ Failed", "No donors available")
            
            return CommResult(
                status="failed",
                message="No donors provided to communicate with",
                attempts=0,
                workflow_time=time.time() - start_time
            )
        
        attempted_donors: List[str] = []
        declined_donors: List[str] = []
        
        donors_to_try = donors[:self.max_donors_to_try]
        
        for index, donor in enumerate(donors_to_try, 1):
            print(f"\n[Communication] 📞 Attempt {index}: {donor.name} ({donor.blood_group})")
            
            if context:
                context.log_event("Communication", f"📞 Attempt {index}", donor.name)
            
            # Query memory before contacting
            if not self._should_contact(donor):
                print(f"[Communication] ⏭️  Skipping {donor.name} (memory cooldown)")
                if context:
                    context.log_event("Communication", "⏭️ Skipped", f"{donor.name} (cooldown)")
                continue
            
            # ✅ Pass attempt number for demo mode
            response = self._contact_donor(donor, request, attempt_number=index)
            attempted_donors.append(donor.name)
            
            # Store interaction in memory
            self._store_interaction(donor, response)
            
            # Handle response
            if response["status"] == "accepted":
                print(f"[Communication] ✅ {donor.name} ACCEPTED!")
                print(f"[Communication] Response: {response['message']}")
                
                if context:
                    context.log_event("Communication", "✅ ACCEPTED", donor.name)
                
                elapsed_time = time.time() - start_time
                return CommResult(
                    status="success",
                    message=f"Donor {donor.name} accepted the request",
                    accepted_donor=donor.name,
                    attempts=index,
                    declined_donors=declined_donors,
                    workflow_time=elapsed_time
                )
            
            elif response["status"] == "declined":
                print(f"[Communication] ❌ {donor.name} DECLINED")
                print(f"[Communication] Response: {response['message']}")
                declined_donors.append(donor.name)
                
                if context:
                    context.log_event("Communication", "❌ DECLINED", donor.name)
            
            elif response["status"] == "no_response":
                print(f"[Communication] ⏰ {donor.name} NO RESPONSE")
                print(f"[Communication] Moving to next donor...")
                declined_donors.append(donor.name)
                
                if context:
                    context.log_event("Communication", "⏰ NO RESPONSE", donor.name)
        
        elapsed_time = time.time() - start_time
        print(f"\n[Communication] ❌ All donors declined or unreachable.")
        
        if context:
            context.log_event("Communication", "❌ FAILED", "All donors declined")
        
        return CommResult(
            status="failed",
            message="No donors accepted the request",
            accepted_donor=None,
            attempts=len(attempted_donors),
            declined_donors=declined_donors,
            workflow_time=elapsed_time
        )
    
    def _contact_donor(self, donor: Donor, request: HospitalRequest, attempt_number: int = 1) -> Dict[str, Any]:
        """
        Simulate contacting a donor.
        
        Args:
            donor: The donor to contact
            request: The hospital request
            attempt_number: Which attempt this is (1 = first donor)
            
        Returns:
            Dict with status and message
        """
        time.sleep(random.uniform(0.1, 0.5))
        random_roll = random.random()
        
        # 🔥 DEMO MODE: First donor always accepts (for reliable demo)
        if attempt_number == 1:
            print(f"[Communication] 🎯 DEMO MODE: First donor always accepts")
            return {
                "status": "accepted",
                "message": f"Donor {donor.name} confirmed they can donate"
            }
        
        base_probability = donor.response_rate
        
        if request.urgency == "Critical":
            base_probability = min(1.0, base_probability * 1.2)
        elif request.urgency == "High":
            base_probability = min(1.0, base_probability * 1.1)
        
        if not donor.available:
            return {
                "status": "declined",
                "message": "Donor is currently unavailable"
            }
        
        if random_roll < base_probability:
            return {
                "status": "accepted",
                "message": f"Donor {donor.name} confirmed they can donate"
            }
        elif random_roll < base_probability + 0.2:
            return {
                "status": "no_response",
                "message": f"{donor.name} did not respond to the notification"
            }
        else:
            return {
                "status": "declined",
                "message": f"{donor.name} cannot donate at this time"
            }
    
    def _should_contact(self, donor: Donor) -> bool:
        """Query memory to check if donor should be contacted."""
        return self.memory_store.should_contact(
            donor_id=donor.id,
            workflow_id=self.workflow_id,
            cooldown_seconds=self.cooldown_seconds
        )
    
    def _store_interaction(self, donor: Donor, response: Dict[str, Any]) -> None:
        """Store donor interaction in memory."""
        status = response["status"]
        
        accepted = status == "accepted"
        declined = status == "declined"
        ignored = status == "no_response"
        
        cooldown_until = None
        if declined or ignored:
            cooldown_until = datetime.now() + timedelta(seconds=self.cooldown_seconds)
        
        memory = DonorMemory(
            donor_id=donor.id,
            last_contacted=datetime.now(),
            accepted=accepted,
            declined=declined,
            ignored=ignored,
            cooldown_until=cooldown_until,
            workflow_id=self.workflow_id,
            last_response=status
        )
        
        self.memory_store.update_donor_memory(donor.id, memory)
        self.contacted_this_session.append(donor.id)