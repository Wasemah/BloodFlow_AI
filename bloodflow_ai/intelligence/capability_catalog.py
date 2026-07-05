"""
Capability Catalog

Lists all system capabilities.
Useful for documentation and for an AI orchestrator.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class Capability:
    """A single system capability."""
    
    name: str
    description: str
    category: str
    status: str = "active"  # active, planned, deprecated
    examples: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "status": self.status,
            "examples": self.examples,
            "tags": self.tags
        }


class CapabilityCatalog:
    """
    Catalog of all system capabilities.
    
    Features:
    - List all capabilities
    - Filter by category
    - Filter by tag
    - Get capability details
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
        self._capabilities: Dict[str, Capability] = {}
        self._initialized = True
        self._build_default_catalog()
    
    def _build_default_catalog(self) -> None:
        """Build the default capability catalog."""
        capabilities = [
            Capability(
                name="Blood Compatibility",
                description="Determines if a donor's blood type is compatible with a patient",
                category="Matching",
                status="active",
                examples=["O- is universal donor", "A+ can receive O+ and A+"],
                tags=["compatibility", "blood", "matching"]
            ),
            Capability(
                name="Donor Eligibility",
                description="Checks donor eligibility including age, cooldown, and availability",
                category="Matching",
                status="active",
                examples=["90-day cooldown period", "Age 18-65 requirement"],
                tags=["eligibility", "cooldown", "age"]
            ),
            Capability(
                name="Donor Ranking",
                description="Ranks donors by compatibility score for optimal selection",
                category="Matching",
                status="active",
                examples=["Highest response rate", "Closest location"],
                tags=["ranking", "scoring", "optimization"]
            ),
            Capability(
                name="Emergency Triage",
                description="Parses unstructured hospital requests into structured data",
                category="Triage",
                status="active",
                examples=["Extract blood type", "Extract hospital name", "Detect urgency"],
                tags=["parsing", "nlp", "extraction"]
            ),
            Capability(
                name="Donor Communication",
                description="Coordinates donor notification with retry logic",
                category="Communication",
                status="active",
                examples=["Contact top donors in order", "Handle acceptance/decline"],
                tags=["communication", "notification", "retry"]
            ),
            Capability(
                name="WHO RAG",
                description="Retrieves relevant WHO blood donation guidelines",
                category="Knowledge",
                status="active",
                examples=["How long to wait between donations", "Antibiotic restrictions"],
                tags=["rag", "retrieval", "knowledge"]
            ),
            Capability(
                name="Cooldown Memory",
                description="Tracks donor cooldown periods to prevent re-contacting",
                category="Memory",
                status="active",
                examples=["Don't contact donor for 1 hour after decline"],
                tags=["memory", "cooldown", "storage"]
            ),
            Capability(
                name="Multi-Agent Orchestration",
                description="Coordinates multiple specialized agents in sequence",
                category="Orchestration",
                status="active",
                examples=["Triage → Matching → Memory → Communication"],
                tags=["orchestration", "coordination", "workflow"]
            ),
            Capability(
                name="Explainability",
                description="Explains why decisions were made",
                category="Observability",
                status="active",
                examples=["Why this donor was selected", "Score breakdown"],
                tags=["explainability", "transparency", "reasoning"]
            ),
            Capability(
                name="Telemetry",
                description="Collects workflow events and performance metrics",
                category="Observability",
                status="active",
                examples=["Workflow timeline", "Agent latency", "Acceptance rate"],
                tags=["metrics", "timeline", "observability"]
            ),
            Capability(
                name="Offline LLM",
                description="Uses local Ollama models for generation without API keys",
                category="AI",
                status="active",
                examples=["Llama 3.2 for RAG", "Nomic embeddings"],
                tags=["llm", "local", "offline"]
            ),
        ]
        
        for cap in capabilities:
            self.register(cap)
    
    def register(self, capability: Capability) -> None:
        """Register a capability."""
        self._capabilities[capability.name] = capability
    
    def get(self, name: str) -> Optional[Capability]:
        """Get a capability by name."""
        return self._capabilities.get(name)
    
    def list_all(self) -> List[Capability]:
        """List all capabilities."""
        return list(self._capabilities.values())
    
    def list_by_category(self, category: str) -> List[Capability]:
        """List capabilities by category."""
        return [
            cap for cap in self._capabilities.values()
            if cap.category.lower() == category.lower()
        ]
    
    def list_by_tag(self, tag: str) -> List[Capability]:
        """List capabilities by tag."""
        return [
            cap for cap in self._capabilities.values()
            if tag.lower() in [t.lower() for t in cap.tags]
        ]
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        return list(set(cap.category for cap in self._capabilities.values()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire catalog to dictionary."""
        return {
            name: cap.to_dict()
            for name, cap in self._capabilities.items()
        }
    
    def generate_markdown(self) -> str:
        """Generate a markdown document of capabilities."""
        lines = ["# BloodFlow AI Capability Catalog\n"]
        
        for category in sorted(self.get_categories()):
            lines.append(f"## {category}\n")
            caps = self.list_by_category(category)
            for cap in caps:
                lines.append(f"### {cap.name}")
                lines.append(f"*{cap.description}*")
                lines.append(f"- Status: {cap.status}")
                if cap.examples:
                    lines.append("- Examples:")
                    for ex in cap.examples:
                        lines.append(f"  - {ex}")
                if cap.tags:
                    lines.append(f"- Tags: {', '.join(cap.tags)}")
                lines.append("")
        
        return "\n".join(lines)
    
    def clear(self) -> None:
        """Clear the catalog and rebuild default."""
        self._capabilities.clear()
        self._build_default_catalog()


# Singleton instance
_catalog: Optional[CapabilityCatalog] = None


def get_capability_catalog() -> CapabilityCatalog:
    """Get the global CapabilityCatalog singleton."""
    global _catalog
    if _catalog is None:
        _catalog = CapabilityCatalog()
    return _catalog