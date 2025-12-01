import uuid
from typing import List
from src.financial_research_agent.models import Trajectory, ResearchStep, ResearchAction, ResearchObservation
from src.financial_research_agent.config import Config

class TrajectoryGenerator:
    def export_trajectory_jsonl(self, trajectory: Trajectory, file_path: str):
        """
        将Trajectory对象导出为JSONL格式，便于SFT/RL训练。
        """
        import json
        with open(file_path, "w", encoding="utf-8") as f:
            traj_dict = trajectory.dict()
            # 步骤拆分为事件流，每步一行
            for step in traj_dict["steps"]:
                event = {
                    "id": traj_dict["id"],
                    "user_query": traj_dict["user_query"],
                    "step": step["step_number"],
                    "thought": step["thought"],
                    "action": step["action"],
                    "observation": step["observation"],
                    "aius_generated": step.get("aius_generated", []),
                }
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            # 最终报告单独一行
            final_event = {
                "id": traj_dict["id"],
                "user_query": traj_dict["user_query"],
                "final_report": traj_dict.get("final_report_content", "")
            }
            f.write(json.dumps(final_event, ensure_ascii=False) + "\n")
    """
    Generates forward cognitive trajectories based on a user query.
    Acts as the 'Teacher' model in the 1.1.1 scheme.
    """
    
    def __init__(self):
        # Initialize LLM client here
        pass

    def generate_step(self, query: str, previous_steps: List[ResearchStep]) -> ResearchStep:
        """
        Simulates one step of the research process.
        In a real implementation, this would call an LLM with the current context.
        """
        step_num = len(previous_steps) + 1
        
        # Placeholder logic for demonstration
        thought = f"Step {step_num}: I need to find more information about {query}."
        action = ResearchAction(
            type="search",
            parameters={"query": f"{query} market size 2025"},
            rationale="Need market sizing data."
        )
        # Simulation of tool execution
        observation = ResearchObservation(
            content="Search results for market size...",
            source_ids=["doc_1"]
        )
        
        return ResearchStep(
            step_number=step_num,
            thought=thought,
            action=action,
            observation=observation
        )

    def generate_forward_trajectory(self, query: str) -> Trajectory:
        """
        Generates a complete trajectory for a given query.
        """
        steps = []
        for i in range(3): # Simulate 3 steps
            step = self.generate_step(query, steps)
            steps.append(step)
            if step.action.type == "stop":
                break
                
        return Trajectory(
            id=str(uuid.uuid4()),
            user_query=query,
            steps=steps,
            final_report_content="Generated report content based on trajectory..."
        )
