from typing import List, Optional
from src.financial_research_agent.models import MemoryItem
from src.financial_research_agent.config import Config

class MemoryManager:
    """
    Hierarchical Recursive Memory Network (HRMN).
    Section 2.1 & 2.3.
    """
    
    def __init__(self):
        self.working_memory: List[MemoryItem] = []
        self.episodic_memory: List[MemoryItem] = []
        self.long_term_memory: List[MemoryItem] = []

    def add_to_working(self, item: MemoryItem):
        self.working_memory.append(item)
        if len(self.working_memory) > Config.WORKING_MEMORY_LIMIT: # conceptual check
            self.compress_working_memory()

    def compress_working_memory(self):
        """
        Moves items from working to episodic memory with summarization.
        """
        # Placeholder: Summarize content using LLM
        summary_item = MemoryItem(
            id="summary_x", 
            content="Summary of previous steps...", 
            type="episodic"
        )
        self.episodic_memory.append(summary_item)
        self.working_memory = [] # Clear working memory or keep only essential

    def recall(self, query: str) -> List[MemoryItem]:
        """
        Retrieves relevant info from episodic/long-term memory.
        """
        # Placeholder: Vector search
        return self.episodic_memory[:2]

    def page_out(self, item_ids: List[str]):
        """
        Explicitly removes items from working memory.
        """
        self.working_memory = [i for i in self.working_memory if i.id not in item_ids]

    def attach_evidence(self, evidence_id: str) -> Optional[MemoryItem]:
        """
        Loads raw evidence for writing/checking.
        """
        # Search in all memories
        all_mem = self.working_memory + self.episodic_memory + self.long_term_memory
        for m in all_mem:
            if m.id == evidence_id:
                return m
        return None
