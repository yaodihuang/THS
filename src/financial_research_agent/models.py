from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class AtomicInsightUnit(BaseModel):
    """
    Atomic Insight Unit (AIU): The smallest unit of information requiring evidence.
    """
    id: str = Field(..., description="Unique identifier for the AIU")
    content: str = Field(..., description="The factual statement or conclusion")
    is_fact: bool = Field(True, description="True if fact, False if conclusion")
    evidence_ids: List[str] = Field(default_factory=list, description="IDs of supporting evidence")
    confidence: float = Field(0.0, description="Confidence score of the AIU")

class ResearchAction(BaseModel):
    """
    An action taken by the agent.
    """
    type: Literal["search", "read", "write", "stop", "plan", "summarize"]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    rationale: str = Field(..., description="Why this action was chosen")

class ResearchObservation(BaseModel):
    """
    The result of an action.
    """
    content: Any
    source_ids: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class ResearchStep(BaseModel):
    """
    A single step in the research trajectory.
    """
    step_number: int
    thought: str
    action: ResearchAction
    observation: ResearchObservation
    aius_generated: List[AtomicInsightUnit] = Field(default_factory=list)

class Trajectory(BaseModel):
    """
    A complete research process trajectory.
    """
    id: str
    user_query: str
    steps: List[ResearchStep]
    final_report_content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReportSection(BaseModel):
    title: str
    content: str
    subsections: List["ReportSection"] = Field(default_factory=list)
    citations: List[str] = Field(default_factory=list)

class FinalReport(BaseModel):
    title: str
    sections: List[ReportSection]
    executive_summary: str
    references: Dict[str, str] = Field(..., description="Map of ID to Citation string")

class MemoryItem(BaseModel):
    """
    Item stored in memory (HRMN).
    """
    id: str
    content: str
    type: Literal["working", "episodic", "long_term"]
    embedding: Optional[List[float]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    access_count: int = 0
