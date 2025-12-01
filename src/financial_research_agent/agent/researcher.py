from typing import List
from src.financial_research_agent.agent.memory import MemoryManager
from src.financial_research_agent.agent.stopping import StoppingPolicy
from src.financial_research_agent.data_pipeline.retrieval import RetrievalSystem
from src.financial_research_agent.models import MemoryItem, ResearchStep, ResearchAction, ResearchObservation
import uuid

class ResearcherAgent:
    """
    Execution Layer: Search, Read, Summarize.
    Section 2.1 & 2.2.
    """
    
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.retrieval = RetrievalSystem()
        self.stopping = StoppingPolicy()

    def execute_task(self, subtask_description: str) -> List[ResearchStep]:
        steps = []
        
        # Initial search
        step = ResearchStep(
            step_number=1,
            thought=f"Starting research for: {subtask_description}",
            action=ResearchAction(type="search", parameters={"query": subtask_description}, rationale="Initial query"),
            observation=ResearchObservation(content="...", source_ids=[])
        )
        
        # Loop until stopping condition
        while not self.stopping.should_stop(step.observation.content):
             # 1. Search
            results = self.retrieval.search(subtask_description) # Simply using description as query for now
            
            # 2. Read & Process (Mock)
            observation_content = f"Processed {len(results)} results."
            
            # 3. Update Memory
            self.memory.add_to_working(MemoryItem(
                id=str(uuid.uuid4()),
                content=observation_content,
                type="working"
            ))
            
            step = ResearchStep(
                step_number=len(steps)+1,
                thought="Found some info, checking if enough.",
                action=ResearchAction(type="read", parameters={}, rationale="Reading results"),
                observation=ResearchObservation(content=observation_content, source_ids=[])
            )
            steps.append(step)
            
            # Safety break for loop
            if len(steps) > 3:
                break
                
        return steps
