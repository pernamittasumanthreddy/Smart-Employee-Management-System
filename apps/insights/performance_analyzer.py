import numpy as np

from apps.insights.models import InsightCategory, InsightSeverity
from apps.performance.models import PerformanceEvaluation


class PerformanceAnalyzer:
    """
    Evaluates multi-cycle appraisal scores using linear trend regression and variance
    to detect upward trajectories or declining performance patterns.
    """

    @classmethod
    def analyze_employee_trends(cls, employee):
        evaluations = PerformanceEvaluation.objects.filter(
            employee=employee,
            is_submitted=True
        ).order_by('cycle__start_date')

        if evaluations.count() < 2:
            return []

        insights = []
        scores = [float(e.final_score) for e in evaluations]
        cycles = [e.cycle.title for e in evaluations]

        # Calculate slope trend using NumPy linear fit
        x = np.arange(len(scores))
        y = np.array(scores)
        slope, _intercept = np.polyfit(x, y, 1)

        latest_score = scores[-1]
        previous_score = scores[-2]

        # 1. Continuous Performance Decline
        if slope < -0.35 or (latest_score < 2.8 and latest_score < previous_score):
            insights.append({
                'category': InsightCategory.PERFORMANCE,
                'severity': InsightSeverity.HIGH,
                'employee': employee,
                'department': employee.department,
                'title': f"Performance Score Decline Trend (Latest: {latest_score}/5.0)",
                'what_detected': f"Appraisal scores for {employee.full_name} have shown a negative downward trajectory over recent review cycles.",
                'why_detected': f"Evaluation slope is negative ({round(slope, 2)} pts/cycle). Score dropped from {previous_score} to {latest_score}.",
                'supporting_data': {
                    'cycle_history': cycles,
                    'score_history': scores,
                    'regression_slope': round(slope, 3),
                    'latest_score': latest_score
                },
                'recommendation': "Formulate a constructive Performance Improvement Plan (PIP) and align on targeted skill training.",
                'confidence_score': 0.93
            })

        # 2. Consistent High Performer / Rapid Ascent
        elif slope > 0.35 or all(s >= 4.3 for s in scores[-2:]):
            insights.append({
                'category': InsightCategory.PERFORMANCE,
                'severity': InsightSeverity.POSITIVE,
                'employee': employee,
                'department': employee.department,
                'title': f"Outstanding High Performer (Score: {latest_score}/5.0)",
                'what_detected': f"{employee.full_name} consistently achieves top-tier appraisal scores across consecutive review periods.",
                'why_detected': f"Multi-cycle score average is {round(np.mean(scores), 2)}/5.0 with positive growth slope ({round(slope, 2)}).",
                'supporting_data': {
                    'cycle_history': cycles,
                    'score_history': scores,
                    'mean_score': round(np.mean(scores), 2)
                },
                'recommendation': "Consider for leadership track promotion, mentorship role, or merit-based recognition awards.",
                'confidence_score': 0.97
            })

        return insights
