"""
Memory Store

Abstract base class and in-memory implementation for donor memory.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from datetime import datetime, timedelta

from bloodflow_ai.schemas.memory_schema import DonorMemory


class MemoryStore(ABC):
    """
    Abstract interface for donor memory storage.
    
    Future implementations:
    - RedisMemoryStore
    - SQLiteMemoryStore
    - PostgreSQLMemoryStore
    """
    
    @abstractmethod
    def get_donor_memory(self, donor_id: int) -> Optional[DonorMemory]:
        """Retrieve memory for a specific donor."""
        pass
    
    @abstractmethod
    def update_donor_memory(self, donor_id: int, memory: DonorMemory) -> None:
        """Update or create memory for a donor."""
        pass
    
    @abstractmethod
    def should_contact(
        self,
        donor_id: int,
        workflow_id: Optional[str] = None,
        cooldown_seconds: int = 3600
    ) -> bool:
        """Check if a donor should be contacted."""
        pass
    
    @abstractmethod
    def reset_workflow_memory(self, workflow_id: str) -> None:
        """Optional: Reset memory for a specific workflow."""
        pass


class InMemoryStore(MemoryStore):
    """In-memory implementation of MemoryStore."""
    
    def __init__(self):
        self._data: Dict[int, DonorMemory] = {}
        self._workflow_data: Dict[str, List[int]] = {}
    
    def get_donor_memory(self, donor_id: int) -> Optional[DonorMemory]:
        """Retrieve memory for a specific donor."""
        return self._data.get(donor_id)
    
    def update_donor_memory(self, donor_id: int, memory: DonorMemory) -> None:
        """Update or create memory for a donor."""
        self._data[donor_id] = memory
        
        if memory.workflow_id:
            if memory.workflow_id not in self._workflow_data:
                self._workflow_data[memory.workflow_id] = []
            if donor_id not in self._workflow_data[memory.workflow_id]:
                self._workflow_data[memory.workflow_id].append(donor_id)
    
    def should_contact(
        self,
        donor_id: int,
        workflow_id: Optional[str] = None,
        cooldown_seconds: int = 3600
    ) -> bool:
        """Check if a donor should be contacted."""
        memory = self._data.get(donor_id)
        
        if not memory:
            return True
        
        if workflow_id and memory.workflow_id == workflow_id and memory.accepted:
            return False
        
        if memory.last_contacted:
            time_diff = (datetime.now() - memory.last_contacted).total_seconds()
            if time_diff < cooldown_seconds:
                return False
        
        if memory.cooldown_until and memory.cooldown_until > datetime.now():
            return False
        
        return True
    
    def reset_workflow_memory(self, workflow_id: str) -> None:
        """Reset memory for a specific workflow."""
        if workflow_id in self._workflow_data:
            for donor_id in self._workflow_data[workflow_id]:
                if donor_id in self._data:
                    self._data[donor_id].workflow_id = None
            del self._workflow_data[workflow_id]
