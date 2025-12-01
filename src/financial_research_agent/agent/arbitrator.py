from typing import List, Dict, Any
from datetime import datetime

class ArbitratorAgent:
    """
    Conflict Resolution & Truth Discovery.
    Section 2.5.
    """
    
    def calculate_confidence(self, source_type: str, date: datetime) -> float:
        """
        来源权威度+时间新鲜度加权。
        """
        base_weight = 0.9 if source_type in ["broker", "consulting"] else 0.3
        months_old = (datetime.now() - date).days / 30
        decay = 0.95 ** months_old
        return base_weight * decay

    def resolve_conflict(self, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        冲突仲裁：来源权威度、时间新鲜度、共识度加权，输出仲裁说明。
        """
        # 统计各value出现次数（共识度）
        value_count = {}
        for point in data_points:
            v = point.get('value')
            value_count[v] = value_count.get(v, 0) + 1
        # 计算每个点的综合分
        scores = []
        for point in data_points:
            conf = self.calculate_confidence(point.get('source_type', 'unknown'), point.get('date', datetime.now()))
            consensus = value_count.get(point.get('value'), 1)
            score = conf * (1 + 0.2 * (consensus - 1))
            scores.append((score, point))
        scores.sort(reverse=True)
        best_point = scores[0][1] if scores else None
        # 仲裁说明
        explanation = f"推荐值{best_point.get('value')}（{value_count.get(best_point.get('value'),1)}家机构一致，最新），"
        if len(value_count) > 1:
            explanation += f"但存在{', '.join(str(v) for v in value_count if v != best_point.get('value'))}保守估计"
        best_point['arbitration_explanation'] = explanation
        return best_point
