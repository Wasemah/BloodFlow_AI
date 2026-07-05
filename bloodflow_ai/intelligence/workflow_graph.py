"""
Workflow Graph

Represents the workflow as a directed graph.
Frontend can animate this. Gemini can inspect it. Reports can visualize it.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """Types of workflow nodes."""
    START = "start"
    AGENT = "agent"
    DECISION = "decision"
    END = "end"
    PARALLEL = "parallel"


@dataclass
class WorkflowNode:
    """A node in the workflow graph."""
    
    id: str
    label: str
    node_type: NodeType
    agent_name: Optional[str] = None
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowEdge:
    """An edge connecting workflow nodes."""
    
    source: str
    target: str
    label: str = ""
    condition: Optional[str] = None


class WorkflowGraph:
    """
    Directed graph representation of the workflow.
    
    Features:
    - Add nodes and edges
    - Serialize to JSON for frontend
    - Get workflow path
    - Validate workflow structure
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
        self._nodes: Dict[str, WorkflowNode] = {}
        self._edges: List[WorkflowEdge] = []
        self._initialized = True
        self._build_default_workflow()
    
    def _build_default_workflow(self) -> None:
        """Build the default workflow graph."""
        # Nodes
        self.add_node(WorkflowNode(
            id="start",
            label="Hospital Request",
            node_type=NodeType.START,
            description="Raw text input from hospital"
        ))
        
        self.add_node(WorkflowNode(
            id="emergency",
            label="Emergency Triage",
            node_type=NodeType.AGENT,
            agent_name="EmergencyTriageAgent",
            description="Parse unstructured hospital request"
        ))
        
        self.add_node(WorkflowNode(
            id="matching",
            label="Donor Matching",
            node_type=NodeType.AGENT,
            agent_name="DonorMatchingAgent",
            description="Filter and rank eligible donors"
        ))
        
        self.add_node(WorkflowNode(
            id="memory",
            label="Memory Check",
            node_type=NodeType.AGENT,
            agent_name="MemoryStore",
            description="Check donor cooldown and history"
        ))
        
        self.add_node(WorkflowNode(
            id="communication",
            label="Communication",
            node_type=NodeType.AGENT,
            agent_name="CommunicationAgent",
            description="Coordinate donor notification"
        ))
        
        self.add_node(WorkflowNode(
            id="end",
            label="Workflow Complete",
            node_type=NodeType.END,
            description="Final response returned"
        ))
        
        # Edges
        self.add_edge(WorkflowEdge("start", "emergency", "Parse request"))
        self.add_edge(WorkflowEdge("emergency", "matching", "Find donors"))
        self.add_edge(WorkflowEdge("matching", "memory", "Check history"))
        self.add_edge(WorkflowEdge("memory", "communication", "Notify donors"))
        self.add_edge(WorkflowEdge("communication", "end", "Complete"))
    
    def add_node(self, node: WorkflowNode) -> None:
        """Add a node to the graph."""
        self._nodes[node.id] = node
    
    def add_edge(self, edge: WorkflowEdge) -> None:
        """Add an edge to the graph."""
        # Validate both nodes exist
        if edge.source not in self._nodes:
            raise ValueError(f"Source node '{edge.source}' not found")
        if edge.target not in self._nodes:
            raise ValueError(f"Target node '{edge.target}' not found")
        
        self._edges.append(edge)
    
    def get_node(self, node_id: str) -> Optional[WorkflowNode]:
        """Get a node by ID."""
        return self._nodes.get(node_id)
    
    def get_edges(self, node_id: str) -> List[WorkflowEdge]:
        """Get all edges from a node."""
        return [e for e in self._edges if e.source == node_id]
    
    def get_path(self, start: str, end: str) -> List[str]:
        """
        Get the path from start to end node.
        
        Args:
            start: Starting node ID
            end: Ending node ID
            
        Returns:
            List of node IDs in order
        """
        if start not in self._nodes or end not in self._nodes:
            return []
        
        path = []
        current = start
        
        while current != end:
            path.append(current)
            edges = self.get_edges(current)
            if not edges:
                break
            current = edges[0].target
        
        path.append(end)
        return path
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the graph to dictionary."""
        return {
            "nodes": [
                {
                    "id": nid,
                    "label": node.label,
                    "type": node.node_type.value,
                    "agent": node.agent_name,
                    "description": node.description
                }
                for nid, node in self._nodes.items()
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "label": edge.label
                }
                for edge in self._edges
            ]
        }
    
    def to_json(self) -> str:
        """Serialize the graph to JSON."""
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    def clear(self) -> None:
        """Clear the graph and rebuild default."""
        self._nodes.clear()
        self._edges.clear()
        self._build_default_workflow()


# Singleton instance
_graph: Optional[WorkflowGraph] = None


def get_workflow_graph() -> WorkflowGraph:
    """Get the global WorkflowGraph singleton."""
    global _graph
    if _graph is None:
        _graph = WorkflowGraph()
    return _graph