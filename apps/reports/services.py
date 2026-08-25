import json

from django.db.models import Avg, Count, Q
from django.utils import timezone

from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.employees.models import Employee, EmploymentStatus
from apps.expenses.models import ExpenseClaim
from apps.helpdesk.models import SupportTicket
from apps.leave_management.models import LeaveRequest
from apps.organization.models import Department
from apps.performance.models import PerformanceEvaluation
from apps.projects.models import Project, ProjectStatus


class ReportAnalyticsService:
    @staticmethod
    def get_executive_overview():
        total_emp = Employee.objects.filter(employment_status=EmploymentStatus.ACTIVE).count()
        active_proj = Project.objects.filter(status=ProjectStatus.ACTIVE).count()
        total_depts = Department.objects.filter(is_active=True).count()
        
        today = timezone.now().date()
        today_att = AttendanceRecord.objects.filter(date=today)
        present_today = today_att.filter(status=AttendanceStatus.PRESENT).count()
        late_today = today_att.filter(is_late=True).count()

        pending_leaves = LeaveRequest.objects.filter(status='PENDING').count()
        pending_expenses = ExpenseClaim.objects.filter(status='PENDING').count()
        open_tickets = SupportTicket.objects.filter(status__in=['OPEN', 'IN_PROGRESS']).count()

        # Department distribution
        dept_dist = Department.objects.filter(is_active=True).annotate(
            emp_count=Count('employees', filter=Q(employees__employment_status=EmploymentStatus.ACTIVE))
        )
        dept_labels = [d.name for d in dept_dist]
        dept_counts = [d.emp_count for d in dept_dist]

        return {
            'total_emp': total_emp,
            'active_proj': active_proj,
            'total_depts': total_depts,
            'present_today': present_today,
            'late_today': late_today,
            'pending_leaves': pending_leaves,
            'pending_expenses': pending_expenses,
            'open_tickets': open_tickets,
            'dept_labels_json': json.dumps(dept_labels),
            'dept_counts_json': json.dumps(dept_counts),
        }

    @staticmethod
    def get_attendance_leave_report_data(start_date=None, end_date=None, dept_id=None):
        records = AttendanceRecord.objects.all()
        if start_date:
            records = records.filter(date__gte=start_date)
        if end_date:
            records = records.filter(date__lte=end_date)
        if dept_id:
            records = records.filter(employee__department_id=dept_id)

        present = records.filter(status=AttendanceStatus.PRESENT).count()
        absent = records.filter(status=AttendanceStatus.ABSENT).count()
        half_day = records.filter(status=AttendanceStatus.HALF_DAY).count()
        late = records.filter(is_late=True).count()

        leave_reqs = LeaveRequest.objects.all()
        if dept_id:
            leave_reqs = leave_reqs.filter(employee__department_id=dept_id)
        
        approved_leaves = leave_reqs.filter(status='APPROVED').count()
        rejected_leaves = leave_reqs.filter(status='REJECTED').count()
        pending_leaves = leave_reqs.filter(status='PENDING').count()

        return {
            'attendance_breakdown': {
                'present': present,
                'absent': absent,
                'half_day': half_day,
                'late': late,
            },
            'leave_breakdown': {
                'approved': approved_leaves,
                'rejected': rejected_leaves,
                'pending': pending_leaves,
            },
            'chart_labels': json.dumps(['Present', 'Absent', 'Half Day', 'Late Arrival']),
            'chart_data': json.dumps([present, absent, half_day, late]),
        }

    @staticmethod
    def get_performance_analytics_data(cycle_id=None, dept_id=None):
        evals = PerformanceEvaluation.objects.filter(is_submitted=True)
        if cycle_id:
            evals = evals.filter(cycle_id=cycle_id)
        if dept_id:
            evals = evals.filter(employee__department_id=dept_id)

        avg_score = evals.aggregate(avg=Avg('final_score'))['avg'] or 0.0
        avg_tech = evals.aggregate(avg=Avg('technical_skills_rating'))['avg'] or 0.0
        avg_comm = evals.aggregate(avg=Avg('communication_rating'))['avg'] or 0.0
        avg_prod = evals.aggregate(avg=Avg('productivity_rating'))['avg'] or 0.0
        avg_lead = evals.aggregate(avg=Avg('leadership_rating'))['avg'] or 0.0

        # Distribution brackets (1-2, 2-3, 3-4, 4-5)
        b1 = evals.filter(final_score__lt=2.0).count()
        b2 = evals.filter(final_score__gte=2.0, final_score__lt=3.0).count()
        b3 = evals.filter(final_score__gte=3.0, final_score__lt=4.0).count()
        b4 = evals.filter(final_score__gte=4.0).count()

        return {
            'avg_score': round(avg_score, 2),
            'avg_tech': round(avg_tech, 2),
            'avg_comm': round(avg_comm, 2),
            'avg_prod': round(avg_prod, 2),
            'avg_lead': round(avg_lead, 2),
            'dist_labels': json.dumps(['< 2.0 (Needs Imp.)', '2.0 - 2.9 (Average)', '3.0 - 3.9 (Proficient)', '4.0 - 5.0 (Exemplary)']),
            'dist_data': json.dumps([b1, b2, b3, b4]),
            'radar_labels': json.dumps(['Technical Skills', 'Communication', 'Productivity', 'Leadership']),
            'radar_data': json.dumps([round(avg_tech, 1), round(avg_comm, 1), round(avg_prod, 1), round(avg_lead, 1)]),
        }
