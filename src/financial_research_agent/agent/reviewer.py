from src.financial_research_agent.models import FinalReport, ReportSection

class ReviewerAgent:
    """
    Execution Layer: Fact checking and structure review.
    """
    
    def review_report(self, report: FinalReport) -> FinalReport:
        """
        Reviews and potentially modifies the report.
        """
        print("[Reviewer] Reviewing report structure and facts...")
        # Placeholder: Logic to check facts against evidence
        
        # Append review note
        report.executive_summary += "\n(Reviewed by ReviewerAgent)"
        return report
