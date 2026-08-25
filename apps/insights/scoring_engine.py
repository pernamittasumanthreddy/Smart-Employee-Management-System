from apps.attendance.models import AttendanceRecord
from apps.goals.models import Goal
from apps.performance.models import PerformanceEvaluation
from apps.tasks.models import Task


class WorkforceScoringEngine:
    """
    Multi-dimensional index calculation for employee productivity,
    engagement, and reliability.
    """

    @classmethod
    def compute_composite_workforce_score(cls, employee):
        # 1. Punctuality / Attendance Score (30%)
        records = AttendanceRecord.objects.filter(employee=employee)
        total_att = records.count()
        if total_att > 0:
            present = records.filter(status='PRESENT').count()
            late = records.filter(is_late=True).count()
            att_score = max(0.0, min(100.0, ((present - (late * 0.5)) / total_att) * 100.0))
        else:
            att_score = 90.0

        # 2. Task Completion Velocity (25%)
        tasks = Task.objects.filter(assigned_to=employee)
        total_tasks = tasks.count()
        if total_tasks > 0:
            completed = tasks.filter(status='COMPLETED').count()
            task_score = (completed / total_tasks) * 100.0
        else:
            task_score = 80.0

        # 3. Appraisal Score Normalized (25%)
        evals = PerformanceEvaluation.objects.filter(employee=employee, is_submitted=True)
        if evals.exists():
            avg_perf = float(evals.latest('cycle__start_date').final_score)
            perf_score = (avg_perf / 5.0) * 100.0
        else:
            perf_score = 75.0

        # 4. Goals Delivery (20%)
        goals = Goal.objects.filter(employee=employee)
        if goals.exists():
            goal_score = float(sum(g.progress_percentage for g in goals) / goals.count())
        else:
            goal_score = 75.0

        composite = (att_score * 0.30) + (task_score * 0.25) + (perf_score * 0.25) + (goal_score * 0.20)
        return {
            'composite_score': round(composite, 1),
            'attendance_score': round(att_score, 1),
            'task_velocity_score': round(task_score, 1),
            'appraisal_score': round(perf_score, 1),
            'goal_score': round(goal_score, 1),
        }
