import math
from typing import List, Dict
from src.financial_research_agent.config import Config

class StoppingPolicy:
    """
    Information Saturation Stopping Policy (ISSP).
    Section 2.4.
    """
    
    def __init__(self):
        self.previous_distribution = {} # Mock distribution of knowledge
        self.steps_taken = 0

    def calculate_information_gain(self, new_info: str) -> float:
        """
        Calculates KL divergence between P_t and P_t+1.
        Mock implementation.
        """
        # In reality: Update entity/topic distribution and compute KL divergence
        # Here: decay based on step count for demo
        return max(0.5 - (self.steps_taken * 0.1), 0.0)

    def should_stop(self, new_info: str) -> bool:
        self.steps_taken += 1
        
        if self.steps_taken >= Config.MAX_STEPS:
            return True
            
        ig = self.calculate_information_gain(new_info)
        return ig < Config.ISSP_THRESHOLD
