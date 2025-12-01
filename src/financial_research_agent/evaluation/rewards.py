from typing import List
from src.financial_research_agent.models import Trajectory, FinalReport

class RewardSystem:
    """
    Multi-objective reward function.
    Section 3.
    """
    
    def calculate_fact_score(self, report: FinalReport) -> float:
        # R_fact: Check evidence binding
        score = 0.0
        # Placeholder logic
        return score

    def calculate_coverage_score(self, report: FinalReport, query: str) -> float:
        # R_coverage: Relevance and checklist completion
        return 0.0

    def calculate_info_density(self, report: FinalReport) -> float:
        # R_info: Avoid redundancy
        return 0.0

    def calculate_structure_score(self, report: FinalReport) -> float:
        # R_struct & R_logic
        return 0.0

    def calculate_total_reward(self, report: FinalReport, query: str) -> float:
        w1, w2, w3, w4 = 1.0, 1.0, 1.0, 1.0
        return (
            w1 * self.calculate_fact_score(report) +
            w2 * self.calculate_coverage_score(report, query) +
            w3 * self.calculate_info_density(report) +
            w4 * self.calculate_structure_score(report)
        )
