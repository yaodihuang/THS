from typing import List
from pydantic import BaseModel

class SubTask(BaseModel):
    id: str
    description: str
    perspective: str # Section 2.2.1 (Technical, Financial, etc.)
    status: str = "pending"

class PlannerAgent:
    """
    Control Layer: Decomposes query into subtasks/outline.
    Section 2.1.
    """
    
    def create_plan(self, user_query: str) -> List[SubTask]:
        """
        Decomposes the user query into a list of subtasks with specific perspectives.
        """
        # Placeholder: LLM call to generate plan
        return [
            SubTask(id="1", description="Analyze Market Size", perspective="Industry"),
            SubTask(id="2", description="Evaluate Key Competitors", perspective="Competition"),
            SubTask(id="3", description="Assess Supply Chain Risks", perspective="Risk"),
            SubTask(id="4", description="Conclude Investment Value", perspective="Financial")
        ]

    def update_plan(self, current_plan: List[SubTask], completed_task_id: str) -> List[SubTask]:
        for task in current_plan:
            if task.id == completed_task_id:
                task.status = "completed"
        return current_plan
