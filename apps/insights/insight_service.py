from apps.employees.models import Employee
from apps.insights.anomaly_detector import AnomalyDetector
from apps.insights.attendance_analyzer import AttendanceAnalyzer
from apps.insights.goal_analyzer import GoalAnalyzer
from apps.insights.models import SmartInsight
from apps.insights.performance_analyzer import PerformanceAnalyzer
from apps.insights.skill_analyzer import SkillAnalyzer
from apps.insights.training_analyzer import TrainingAnalyzer
from apps.insights.workload_analyzer import WorkloadAnalyzer


class SmartInsightService:
    """
    Orchestration service that triggers all local mathematical, statistical,
    and machine learning analyzers across the platform and persists explainable insights.
    """

    @classmethod
    def run_full_system_analysis(cls):
        all_raw_insights = []

        # 1. Workload analysis
        all_raw_insights.extend(WorkloadAnalyzer.analyze_workload_health())

        # 2. Skill gaps
        all_raw_insights.extend(SkillAnalyzer.analyze_project_skill_gaps())

        # 3. Goal trajectories
        all_raw_insights.extend(GoalAnalyzer.analyze_goal_trajectories())

        # 4. Expense anomalies
        all_raw_insights.extend(AnomalyDetector.detect_expense_anomalies())

        # 5. Employee specific analyzers
        active_employees = Employee.objects.filter(employment_status='ACTIVE')
        for emp in active_employees:
            all_raw_insights.extend(AttendanceAnalyzer.analyze_employee_attendance(emp))
            all_raw_insights.extend(PerformanceAnalyzer.analyze_employee_trends(emp))
            all_raw_insights.extend(TrainingAnalyzer.analyze_training_needs(emp))

        # Clear outdated active insights and persist newly generated ones
        SmartInsight.objects.filter(is_dismissed=False).delete()

        created_objs = []
        for raw in all_raw_insights:
            obj = SmartInsight(
                category=raw['category'],
                severity=raw['severity'],
                title=raw['title'],
                employee=raw.get('employee'),
                department=raw.get('department'),
                what_detected=raw['what_detected'],
                why_detected=raw['why_detected'],
                supporting_data=raw.get('supporting_data', {}),
                recommendation=raw['recommendation'],
                confidence_score=raw.get('confidence_score', 0.90)
            )
            created_objs.append(obj)

        SmartInsight.objects.bulk_create(created_objs)
        return len(created_objs)
