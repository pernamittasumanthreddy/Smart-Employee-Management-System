from django.utils import timezone

from apps.goals.models import Goal, GoalStatus
from apps.insights.models import InsightCategory, InsightSeverity


class GoalAnalyzer:
    """
    Goal trajectory analyzer calculating progress velocity against remaining timeline
    to detect delayed and at-risk corporate goals.
    """

    @classmethod
    def analyze_goal_trajectories(cls):
        active_goals = Goal.objects.filter(status=GoalStatus.IN_PROGRESS).select_related('employee__department', 'team')
        today = timezone.now().date()
        insights = []

        for goal in active_goals:
            total_duration = (goal.due_date - goal.start_date).days if goal.due_date > goal.start_date else 1
            elapsed_days = (today - goal.start_date).days
            days_remaining = (goal.due_date - today).days

            if total_duration <= 0 or elapsed_days <= 0:
                continue

            expected_progress = min(100, (elapsed_days / total_duration) * 100)
            actual_progress = goal.progress_percentage
            progress_deficit = expected_progress - actual_progress

            # Goal at severe risk: 70%+ of time elapsed, but progress is less than 40%
            if (elapsed_days / total_duration) >= 0.60 and progress_deficit >= 25.0 and days_remaining > 0:
                insights.append({
                    'category': InsightCategory.GOAL,
                    'severity': InsightSeverity.HIGH,
                    'employee': goal.employee,
                    'department': goal.employee.department if goal.employee else (goal.team.department if goal.team else None),
                    'title': f"Goal Delivery At Risk: '{goal.title}' ({actual_progress}% vs expected {round(expected_progress)}%)",
                    'what_detected': f"Goal '{goal.title}' is trailing expected progress trajectory with only {days_remaining} days remaining.",
                    'why_detected': f"{round((elapsed_days / total_duration) * 100)}% of timeline elapsed, but goal progress is at {actual_progress}% (Deficit: {round(progress_deficit)}%).",
                    'supporting_data': {
                        'goal_id': goal.id,
                        'actual_progress': actual_progress,
                        'expected_progress': round(expected_progress, 1),
                        'days_remaining': days_remaining,
                        'due_date': str(goal.due_date)
                    },
                    'recommendation': "Conduct an immediate milestone check-in, remove blockers, or adjust the target key result deliverables.",
                    'confidence_score': 0.93
                })

            # Goal Achieved early
            elif actual_progress >= 100 and days_remaining >= 7:
                insights.append({
                    'category': InsightCategory.GOAL,
                    'severity': InsightSeverity.POSITIVE,
                    'employee': goal.employee,
                    'department': goal.employee.department if goal.employee else None,
                    'title': f"Goal Completed Ahead of Schedule: '{goal.title}'",
                    'what_detected': f"Target milestones achieved {days_remaining} days ahead of scheduled deadline.",
                    'why_detected': f"100% completion verified prior to target date ({goal.due_date}).",
                    'supporting_data': {
                        'days_early': days_remaining,
                        'completed_date': str(today)
                    },
                    'recommendation': "Mark goal as officially achieved and acknowledge contributor performance during next review.",
                    'confidence_score': 0.98
                })

        return insights
