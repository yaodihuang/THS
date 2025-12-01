from src.financial_research_agent.models import ReportSection, MemoryItem
from src.financial_research_agent.agent.memory import MemoryManager
from typing import List

class WriterAgent:
    """
    Execution Layer: Writes chapters based on outline and memory.
    """
    
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def write_section(self, section_title: str, relevant_memories: List[MemoryItem]) -> ReportSection:
        """
        Generates a report section.
        """
        # Placeholder: LLM generation based on memories
        content = f"This is the content for section {section_title}.\n"
        content += "Based on the following evidence:\n"
        for mem in relevant_memories:
            content += f"- {mem.content}\n"
            
        return ReportSection(
            title=section_title,
            content=content,
            subsections=[],
            citations=[m.id for m in relevant_memories]
        )

