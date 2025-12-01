from typing import List
from src.financial_research_agent.models import Trajectory, FinalReport

class RewardSystem:
    """
    Multi-objective reward function.
    Section 3.
    """
    
    def calculate_fact_score(self, report: FinalReport) -> float:
        """
        R_fact: 所有实体、数值、日期、指标必须绑定证据片段ID。
        每有证据绑定+0.2分，无证据-0.1分，冲突/无关-0.5分（此处简化为无证据-0.1分）。
        """
        score = 0.0
        total_aiu = 0
        for section in report.sections:
            for subsection in section.subsections:
                for aiu_id in subsection.citations:
                    total_aiu += 1
                    if aiu_id in report.references:
                        score += 0.2
                    else:
                        score -= 0.1
        if total_aiu == 0:
            return 0.0
        return score / total_aiu

    def calculate_coverage_score(self, report: FinalReport, query: str) -> float:
        """
        R_coverage: 相关性与覆盖度。标题与Query相关度，章节覆盖关键问题。
        """
        score = 0.0
        # 简单相关性：标题包含Query关键词+0.5分
        if query and query in report.title:
            score += 0.5
        # 覆盖度：每个section标题包含行业、竞争、估值、风险等关键词+0.25分
        checklist = ["市场", "竞争", "估值", "风险"]
        for section in report.sections:
            for key in checklist:
                if key in section.title:
                    score += 0.25
        return min(score, 1.0)

    def calculate_info_density(self, report: FinalReport) -> float:
        """
        R_info: 信息密度=有效信息单元数/文字长度，语义重复惩罚。
        """
        total_length = sum(len(section.content) for section in report.sections)
        total_aiu = sum(len(section.citations) for section in report.sections)
        if total_length == 0:
            return 0.0
        density = total_aiu / total_length
        # 密度大于0.01奖励+1分，过小-1分
        if density > 0.01:
            return 1.0
        else:
            return -1.0

    def calculate_structure_score(self, report: FinalReport) -> float:
        """
        R_struct & R_logic: 检查章节顺序与逻辑连贯性。
        """
        outline = ["综述", "产业链", "公司", "风险", "结论"]
        titles = [section.title for section in report.sections]
        # 顺序正确+1分，错位-0.5分
        if titles[:len(outline)] == outline:
            score = 1.0
        else:
            score = -0.5
        return score

    def calculate_total_reward(self, report: FinalReport, query: str) -> float:
        w1, w2, w3, w4 = 1.0, 1.0, 1.0, 1.0
        return (
            w1 * self.calculate_fact_score(report) +
            w2 * self.calculate_coverage_score(report, query) +
            w3 * self.calculate_info_density(report) +
            w4 * self.calculate_structure_score(report)
        )
