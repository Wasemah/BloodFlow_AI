"""
Agent Registry

Stores metadata for every agent in the system.
Acts as a directory of agents, not an execution engine.
"""

from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentMetadata:
    """Metadata for a single agent."""
    
    name: str
    description: str
    input_schema: str
    output_schema: str
    capabilities: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    status: str = "active"  # active, deprecated, experimental
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "capabilities": self.capabilities,
            "version": self.version,
            "status": self.status
        }


class AgentRegistry:
    """
    Registry of all agents in the system.
    
    Features:
    - Register agents with metadata
    - Look up agents by name
    - List all agents
    - Filter agents by capability
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._agents: Dict[str, AgentMetadata] = {}
        self._initialized = True
    
    def register(self, metadata: AgentMetadata) -> None:
        """
        Register an agent in the registry.
        
        Args:
            metadata: Agent metadata to register
        """
        self._agents[metadata.name] = metadata
        print(f"[AgentRegistry] ✅ Registered: {metadata.name}")
    
    def register_from_class(self, agent_class: Type, name: str, description: str, **kwargs) -> None:
        """
        Register an agent from a class.
        
        Args:
            agent_class: The agent class
            name: Agent name
            description: Agent description
            **kwargs: Additional metadata
        """
        # Try to infer schemas from class
        input_schema = getattr(agent_class, "input_schema", "Unknown")
        output_schema = getattr(agent_class, "output_schema", "Unknown")
        
        metadata = AgentMetadata(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            capabilities=kwargs.get("capabilities", []),
            version=kwargs.get("version", "1.0.0"),
            status=kwargs.get("status", "active")
        )
        self.register(metadata)
    
    def get(self, name: str) -> Optional[AgentMetadata]:
        """Get agent metadata by name."""
        return self._agents.get(name)
    
    def list_all(self) -> List[AgentMetadata]:
        """List all registered agents."""
        return list(self._agents.values())
    
    def list_by_capability(self, capability: str) -> List[AgentMetadata]:
        """List agents with a specific capability."""
        return [
            agent for agent in self._agents.values()
            if capability in agent.capabilities
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire registry to dictionary."""
        return {
            name: metadata.to_dict()
            for name, metadata in self._agents.items()
        }
    
    def clear(self) -> None:
        """Clear the registry."""
        self._agents.clear()


# Singleton instance
_registry: Optional[AgentRegistry] = None


def get_agent_registry() -> AgentRegistry:
    """Get the global AgentRegistry singleton."""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry