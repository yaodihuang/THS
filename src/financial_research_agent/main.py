import uuid
from src.financial_research_agent.agent.planner import PlannerAgent
from src.financial_research_agent.agent.researcher import ResearcherAgent
from src.financial_research_agent.agent.writer import WriterAgent
from src.financial_research_agent.agent.reviewer import ReviewerAgent
from src.financial_research_agent.agent.memory import MemoryManager
from src.financial_research_agent.models import FinalReport

def main():
    user_query = "Analyze the investment opportunities in the humanoid robot industry in 2025"
    print(f"=== Starting Financial Research Agent ===")
    print(f"Query: {user_query}\n")

    # 1. Initialize Agents
    memory = MemoryManager()
    planner = PlannerAgent()
    researcher = ResearcherAgent(memory)
    writer = WriterAgent(memory)
    reviewer = ReviewerAgent()

    # 2. Plan
    print("--- Planning ---")
    subtasks = planner.create_plan(user_query)
    for task in subtasks:
        print(f"Subtask: {task.description} ({task.perspective})")

    # 3. Execute & Research
    print("\n--- Researching ---")
    for task in subtasks:
        print(f"Researching: {task.description}...")
        steps = researcher.execute_task(task.description)
        # In a real system, steps would populate memory automatically or we'd do it here explicitly
        # (ResearcherAgent already adds to memory in our mock)

    # 4. Write
    print("\n--- Writing ---")
    sections = []
    for task in subtasks:
        # Recall relevant info for this specific section
        # In a real system, we'd filter memory by relevance to the task
        relevant_mems = memory.working_memory + memory.episodic_memory 
        section = writer.write_section(task.description, relevant_mems)
        sections.append(section)
        print(f"Generated section: {section.title}")

    # 5. Review & Assemble
    print("\n--- Reviewing ---")
    final_report = FinalReport(
        title=f"Investment Analysis: {user_query}",
        sections=sections,
        executive_summary="This is a generated executive summary.",
        references={}
    )
    
    final_report = reviewer.review_report(final_report)

    # Output
    print("\n=== Final Report ===")
    print(f"Title: {final_report.title}")
    print(f"Executive Summary: {final_report.executive_summary}")
    for sec in final_report.sections:
        print(f"\n## {sec.title}")
        print(sec.content[:100] + "...") # Truncate for display

if __name__ == "__main__":
    main()
