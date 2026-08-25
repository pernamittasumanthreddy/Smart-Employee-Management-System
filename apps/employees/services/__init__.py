from django.utils import timezone

from apps.employees.models import (
    Employee,
)


class Employee360Service:
    """
    Centralized service that dynamically compiles the complete 360-degree profile
    of an employee across all 24 modules of the platform.
    """

    @staticmethod
    def get_full_360_profile(employee_id):
        if hasattr(employee_id, 'id'):
            employee_id = employee_id.id
        try:
            employee = Employee.objects.select_related(
                'user', 'department', 'team', 'designation', 'reporting_manager'
            ).prefetch_related(
                'educations', 'experiences', 'direct_reports'
            ).get(id=employee_id)
        except Employee.DoesNotExist:
            return None

        # 1. Personal & Org Details
        bank = getattr(employee, 'bank_details', None)

        # 2. Attendance Summary
        attendance_records = getattr(employee, 'attendance_records', None)
        att_total = attendance_records.count() if attendance_records else 0
        att_present = attendance_records.filter(status='PRESENT').count() if attendance_records else 0
        att_late = attendance_records.filter(is_late=True).count() if attendance_records else 0
        att_absent = attendance_records.filter(status='ABSENT').count() if attendance_records else 0
        att_halfday = attendance_records.filter(status='HALF_DAY').count() if attendance_records else 0
        punctuality_rate = round((att_present - att_late) / att_present * 100, 1) if att_present > 0 else 100.0

        # 3. Leave Summary
        leave_balances = getattr(employee, 'leave_balances', None)
        leave_requests = getattr(employee, 'leave_requests', None)
        approved_leaves = leave_requests.filter(status='APPROVED').count() if leave_requests else 0
        pending_leaves = leave_requests.filter(status='PENDING').count() if leave_requests else 0

        # 4. Projects & Tasks
        assigned_tasks = getattr(employee, 'assigned_tasks', None)
        total_tasks = assigned_tasks.count() if assigned_tasks else 0
        completed_tasks = assigned_tasks.filter(status='COMPLETED').count() if assigned_tasks else 0
        in_progress_tasks = assigned_tasks.filter(status='IN_PROGRESS').count() if assigned_tasks else 0
        overdue_tasks = assigned_tasks.filter(status__in=['TODO', 'IN_PROGRESS'], due_date__lt=timezone.now().date()).count() if assigned_tasks else 0

        # 5. Workload
        workload_record = getattr(employee, 'workload_metric', None)
        workload_score = workload_record.workload_score if workload_record else 0

        # 6. Skills Matrix
        employee_skills = getattr(employee, 'skills', None)
        skills_list = employee_skills.select_related('skill').all() if employee_skills else []

        # 7. Goals
        goals = getattr(employee, 'goals', None)
        goals_list = goals.all() if goals else []
        avg_goal_progress = round(sum(g.progress_percentage for g in goals_list) / len(goals_list), 1) if goals_list else 0

        # 8. Performance Reviews
        evaluations = getattr(employee, 'performance_evaluations', None)
        perf_reviews = evaluations.select_related('cycle', 'evaluator').order_by('-cycle__start_date') if evaluations else []
        latest_score = perf_reviews.first().final_score if (perf_reviews and perf_reviews.first()) else None

        # 9. Training & Certifications
        trainings = getattr(employee, 'training_enrollments', None)
        training_list = trainings.select_related('course').all() if trainings else []

        # 10. Recognitions & Kudos
        recognitions = getattr(employee, 'recognitions_received', None)
        recognition_list = recognitions.select_related('sender').all() if recognitions else []

        # 11. Assets Assigned
        assets = getattr(employee, 'assigned_assets', None)
        asset_list = assets.select_related('category').all() if assets else []

        # 12. Expenses
        expenses = getattr(employee, 'expenses', None)
        expense_list = expenses.all() if expenses else []
        total_reimbursed = sum(e.amount for e in expense_list.filter(status='REIMBURSED')) if expenses else 0

        # 13. Helpdesk Support Tickets
        tickets = getattr(employee, 'tickets_created', None)
        ticket_list = tickets.all() if tickets else []

        # 14. Documents
        documents = getattr(employee, 'documents', None)
        doc_list = documents.all() if documents else []

        return {
            'employee': employee,
            'bank': bank,
            'attendance': {
                'total': att_total,
                'present': att_present,
                'late': att_late,
                'absent': att_absent,
                'half_day': att_halfday,
                'punctuality_rate': punctuality_rate,
                'recent': attendance_records.order_by('-date')[:7] if attendance_records else []
            },
            'leave': {
                'balances': leave_balances.select_related('leave_type').all() if leave_balances else [],
                'approved_count': approved_leaves,
                'pending_count': pending_leaves,
                'recent': leave_requests.order_by('-start_date')[:5] if leave_requests else []
            },
            'tasks': {
                'total': total_tasks,
                'completed': completed_tasks,
                'in_progress': in_progress_tasks,
                'overdue': overdue_tasks,
                'list': assigned_tasks.order_by('due_date')[:10] if assigned_tasks else []
            },
            'workload_score': workload_score,
            'skills': skills_list,
            'goals': {
                'list': goals_list,
                'avg_progress': avg_goal_progress
            },
            'performance': {
                'reviews': perf_reviews,
                'latest_score': latest_score
            },
            'training': training_list,
            'recognitions': recognition_list,
            'assets': asset_list,
            'expenses': {
                'list': expense_list.order_by('-expense_date')[:5] if expenses else [],
                'total_reimbursed': total_reimbursed
            },
            'tickets': ticket_list.order_by('-created_at')[:5] if tickets else [],
            'documents': doc_list,
        }
