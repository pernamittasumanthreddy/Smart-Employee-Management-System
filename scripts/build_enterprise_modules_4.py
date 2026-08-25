import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# 6. APPS / TIMESHEETS (Client Billing & Project Hours)
# ==============================================================================

write_file("apps/timesheets/__init__.py", """default_app_config = 'apps.timesheets.apps.TimesheetsConfig'""")

write_file("apps/timesheets/apps.py", """
from django.apps import AppConfig

class TimesheetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.timesheets'
    verbose_name = 'Enterprise Client Timesheets & Billable Hours'
""")

write_file("apps/timesheets/models.py", """
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee
from apps.projects.models import Project

class ClientRateCard(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rate_cards')
    role_name = models.CharField(max_length=150, help_text="e.g. Lead Architect, Senior Fullstack Engineer")
    hourly_billable_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('85.00'))
    currency = models.CharField(max_length=10, default="USD")
    effective_start = models.DateField()
    effective_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.role_name} ({self.currency} {self.hourly_billable_rate}/hr)"


class WeeklyTimesheet(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft / Editing'), ('SUBMITTED', 'Submitted to Manager'), ('APPROVED', 'Approved by Manager'), ('REJECTED', 'Rejected / Revisions Requested')]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='weekly_timesheets')
    week_start_date = models.DateField(help_text="Monday date of the week")
    week_end_date = models.DateField(help_text="Sunday date of the week")
    total_billable_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('40.00'))
    total_non_billable_hours = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_timesheets')
    approver_comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'week_start_date')
        ordering = ['-week_start_date']

    def __str__(self):
        return f"Timesheet: {self.employee.full_name} ({self.week_start_date} to {self.week_end_date}) [{self.status}]"

    @property
    def total_hours(self):
        return self.total_billable_hours + self.total_non_billable_hours


class TimesheetEntry(models.Model):
    timesheet = models.ForeignKey(WeeklyTimesheet, on_delete=models.CASCADE, related_name='entries')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    entry_date = models.DateField()
    hours_logged = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('8.00'))
    is_billable = models.BooleanField(default=True)
    task_description = models.TextField(help_text="Detailed summary of deliverables worked on")
    jira_or_ticket_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.entry_date} - {self.project.name} ({self.hours_logged} hrs)"
""")

write_file("apps/timesheets/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.timesheets.models import WeeklyTimesheet, TimesheetEntry, ClientRateCard
from apps.projects.models import Project

@login_required
def timesheets_dashboard(request):
    timesheets = WeeklyTimesheet.objects.select_related('employee', 'approver').all()[:10]
    projects = Project.objects.all()[:5]
    user_timesheets = []
    if hasattr(request.user, 'employee_profile'):
        user_timesheets = WeeklyTimesheet.objects.filter(employee=request.user.employee_profile)[:6]

    context = {
        'timesheets': timesheets,
        'projects': projects,
        'user_timesheets': user_timesheets,
    }
    return render(request, 'timesheets/dashboard.html', context)

@login_required
def timesheet_detail(request, pk):
    timesheet = get_object_or_404(WeeklyTimesheet.objects.select_related('employee'), pk=pk)
    entries = timesheet.entries.select_related('project')
    return render(request, 'timesheets/timesheet_detail.html', {'timesheet': timesheet, 'entries': entries})

@login_required
def timesheet_approval(request, pk):
    timesheet = get_object_or_404(WeeklyTimesheet, pk=pk)
    timesheet.status = 'APPROVED'
    if hasattr(request.user, 'employee_profile'):
        timesheet.approver = request.user.employee_profile
    timesheet.save()
    messages.success(request, f"Timesheet for {timesheet.employee.full_name} approved successfully.")
    return redirect('timesheets:timesheet_detail', pk=timesheet.pk)
""")

write_file("apps/timesheets/urls.py", """
from django.urls import path
from apps.timesheets import views

app_name = 'timesheets'

urlpatterns = [
    path('', views.timesheets_dashboard, name='dashboard'),
    path('<int:pk>/', views.timesheet_detail, name='timesheet_detail'),
    path('<int:pk>/approve/', views.timesheet_approval, name='timesheet_approval'),
]
""")

write_file("apps/timesheets/admin.py", """
from django.contrib import admin
from apps.timesheets.models import ClientRateCard, WeeklyTimesheet, TimesheetEntry

@admin.register(ClientRateCard)
class ClientRateCardAdmin(admin.ModelAdmin):
    list_display = ('project', 'role_name', 'hourly_billable_rate', 'currency')

@admin.register(WeeklyTimesheet)
class WeeklyTimesheetAdmin(admin.ModelAdmin):
    list_display = ('employee', 'week_start_date', 'total_billable_hours', 'status')
    list_filter = ('status',)

@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ('timesheet', 'project', 'entry_date', 'hours_logged', 'is_billable')
""")

# ==============================================================================
# 7. APPS / SURVEYS (eNPS, Team Morale & Pulse Surveys)
# ==============================================================================

write_file("apps/surveys/__init__.py", """default_app_config = 'apps.surveys.apps.SurveysConfig'""")

write_file("apps/surveys/apps.py", """
from django.apps import AppConfig

class SurveysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.surveys'
    verbose_name = 'Employee Surveys, eNPS & Pulse Feedback'
""")

write_file("apps/surveys/models.py", """
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class Survey(models.Model):
    SURVEY_TYPES = [('ENPS', 'eNPS Quarterly Workforce Survey'), ('PULSE', 'Monthly Morale Pulse Check'), ('ONBOARDING', '30-Day Onboarding Feedback'), ('EXIT', 'Confidential Exit Survey'), ('CUSTOM', 'Custom Organizational Survey')]

    title = models.CharField(max_length=200)
    survey_type = models.CharField(max_length=30, choices=SURVEY_TYPES, default='ENPS')
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    is_anonymous = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    target_responses_count = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_survey_type_display()})"


class SurveyQuestion(models.Model):
    QUESTION_TYPES = [('RATING_10', '1-10 Scale (eNPS)'), ('RATING_5', '1-5 Stars (Likert Scale)'), ('TEXT', 'Open-Ended Qualitative Text'), ('CHOICE', 'Multiple Choice Single Selection')]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField(default=1)
    prompt_text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default='RATING_10')
    choices_csv = models.CharField(max_length=255, blank=True, help_text="Comma separated options if Multiple Choice")
    is_required = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.prompt_text}"


class SurveySubmission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='submissions')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, help_text="Null if 100% anonymous")
    submitted_at = models.DateTimeField(auto_now_add=True)
    enps_score = models.IntegerField(null=True, blank=True, help_text="0-10 rating")
    qualitative_feedback = models.TextField(blank=True)
    sentiment_label = models.CharField(max_length=30, choices=[('POSITIVE', 'Promoter / High Satisfaction'), ('PASSIVE', 'Passive / Neutral'), ('DETRACTOR', 'Detractor / At-Risk')], default='POSITIVE')

    def __str__(self):
        return f"Submission #{self.id} for {self.survey.title} ({self.sentiment_label})"
""")

write_file("apps/surveys/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission

@login_required
def survey_dashboard(request):
    surveys = Survey.objects.filter(is_active=True)
    recent_submissions = SurveySubmission.objects.all().order_by('-submitted_at')[:8]
    
    # Calculate eNPS score
    submissions = SurveySubmission.objects.filter(enps_score__isnull=False)
    total = submissions.count()
    promoters = submissions.filter(enps_score__gte=9).count()
    detractors = submissions.filter(enps_score__lte=6).count()
    enps_index = int(((promoters - detractors) / total) * 100) if total > 0 else 72

    context = {
        'surveys': surveys,
        'recent_submissions': recent_submissions,
        'total_submissions': total,
        'enps_index': enps_index,
        'promoters_count': promoters,
        'detractors_count': detractors,
    }
    return render(request, 'surveys/dashboard.html', context)

@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    questions = survey.questions.all()
    return render(request, 'surveys/survey_detail.html', {'survey': survey, 'questions': questions})
""")

write_file("apps/surveys/urls.py", """
from django.urls import path
from apps.surveys import views

app_name = 'surveys'

urlpatterns = [
    path('', views.survey_dashboard, name='dashboard'),
    path('<int:pk>/', views.survey_detail, name='survey_detail'),
]
""")

write_file("apps/surveys/admin.py", """
from django.contrib import admin
from apps.surveys.models import Survey, SurveyQuestion, SurveySubmission

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'survey_type', 'start_date', 'end_date', 'is_anonymous', 'is_active')

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'order', 'prompt_text', 'question_type')

@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'submitted_at', 'enps_score', 'sentiment_label')
""")

# ==============================================================================
# 8. APPS / WORKPLACE (Travel, Desks & Visitor Passes)
# ==============================================================================

write_file("apps/workplace/__init__.py", """default_app_config = 'apps.workplace.apps.WorkplaceConfig'""")

write_file("apps/workplace/apps.py", """
from django.apps import AppConfig

class WorkplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.workplace'
    verbose_name = 'Smart Workplace, Desk Booking & Travel Requests'
""")

write_file("apps/workplace/models.py", """
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class TravelRequest(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending Manager Approval'), ('APPROVED', 'Approved & Booked'), ('REJECTED', 'Rejected'), ('COMPLETED', 'Travel Completed')]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='travel_requests')
    purpose = models.CharField(max_length=200, help_text="e.g. AWS Summit London 2026, Client On-site Workshop")
    origin_city = models.CharField(max_length=100, default="Bengaluru")
    destination_city = models.CharField(max_length=100, default="San Francisco / London")
    departure_date = models.DateField()
    return_date = models.DateField()
    flight_preference = models.CharField(max_length=100, default="Economy Non-stop")
    hotel_needed = models.BooleanField(default=True)
    advance_cash_requested = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('50000.00'))
    estimated_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('180000.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    manager_approval_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Travel: {self.employee.full_name} -> {self.destination_city} ({self.departure_date})"


class DeskBooking(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='desk_bookings')
    building = models.CharField(max_length=100, default="Tower Alpha")
    floor = models.CharField(max_length=50, default="Floor 4 - Tech Hub")
    desk_number = models.CharField(max_length=30, default="DESK-4A-12")
    booking_date = models.DateField(default=timezone.now)
    time_slot = models.CharField(max_length=30, choices=[('FULL_DAY', 'Full Day (9 AM - 6 PM)'), ('MORNING', 'Morning (8 AM - 1 PM)'), ('EVENING', 'Afternoon/Evening (1 PM - 8 PM)')], default='FULL_DAY')
    has_dual_monitors = models.BooleanField(default=True)
    is_checked_in = models.BooleanField(default=True)

    class Meta:
        unique_together = ('building', 'floor', 'desk_number', 'booking_date', 'time_slot')

    def __str__(self):
        return f"{self.desk_number} - {self.employee.full_name} ({self.booking_date})"


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Aryabhata Boardroom, Ramanujan Brainstorm Pod")
    building = models.CharField(max_length=100, default="Tower Alpha")
    floor = models.CharField(max_length=50, default="Floor 3")
    capacity_seats = models.IntegerField(default=12)
    has_video_conferencing = models.BooleanField(default=True)
    has_whiteboard = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.capacity_seats} Seats, {self.floor})"


class VisitorPass(models.Model):
    visitor_name = models.CharField(max_length=150)
    visitor_company = models.CharField(max_length=150, default="External Partner / Client")
    visitor_email = models.EmailField()
    visitor_phone = models.CharField(max_length=30)
    host_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='hosted_visitors')
    visit_date = models.DateField(default=timezone.now)
    pass_code = models.CharField(max_length=50, unique=True)
    purpose = models.CharField(max_length=200, default="Quarterly Strategic Planning")
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    badge_number = models.CharField(max_length=30, default="VIS-042")

    def __str__(self):
        return f"Visitor: {self.visitor_name} -> Host: {self.host_employee.full_name}"
""")

write_file("apps/workplace/views.py", """
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.workplace.models import TravelRequest, DeskBooking, MeetingRoom, VisitorPass

@login_required
def workplace_dashboard(request):
    travel_requests = TravelRequest.objects.select_related('employee').all()[:6]
    desk_bookings = DeskBooking.objects.select_related('employee').all()[:8]
    meeting_rooms = MeetingRoom.objects.filter(is_active=True)
    visitors = VisitorPass.objects.select_related('host_employee').all()[:6]

    context = {
        'travel_requests': travel_requests,
        'desk_bookings': desk_bookings,
        'meeting_rooms': meeting_rooms,
        'visitors': visitors,
    }
    return render(request, 'workplace/dashboard.html', context)

@login_required
def travel_list(request):
    travels = TravelRequest.objects.select_related('employee')
    return render(request, 'workplace/travel_list.html', {'travels': travels})

@login_required
def desk_booking_portal(request):
    bookings = DeskBooking.objects.select_related('employee').all()[:20]
    return render(request, 'workplace/desk_booking.html', {'bookings': bookings})
""")

write_file("apps/workplace/urls.py", """
from django.urls import path
from apps.workplace import views

app_name = 'workplace'

urlpatterns = [
    path('', views.workplace_dashboard, name='dashboard'),
    path('travel/', views.travel_list, name='travel_list'),
    path('desks/', views.desk_booking_portal, name='desk_booking'),
]
""")

write_file("apps/workplace/admin.py", """
from django.contrib import admin
from apps.workplace.models import TravelRequest, DeskBooking, MeetingRoom, VisitorPass

@admin.register(TravelRequest)
class TravelRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'purpose', 'destination_city', 'departure_date', 'status')

@admin.register(DeskBooking)
class DeskBookingAdmin(admin.ModelAdmin):
    list_display = ('desk_number', 'employee', 'building', 'floor', 'booking_date')

@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'capacity_seats', 'has_video_conferencing')

@admin.register(VisitorPass)
class VisitorPassAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'host_employee', 'visit_date', 'badge_number')
""")

# ==============================================================================
# 9. APPS / API (RESTful API, Webhooks & Integrations)
# ==============================================================================

write_file("apps/api/__init__.py", """default_app_config = 'apps.api.apps.ApiConfig'""")

write_file("apps/api/apps.py", """
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'
    verbose_name = 'Enterprise Developer REST API & Webhook Suite'
""")

write_file("apps/api/models.py", """
import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone

class APIKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100, help_text="e.g. Biometric Attendance Sync Service, Mobile App Gateway")
    key = models.CharField(max_length=64, unique=True, default=secrets.token_hex)
    is_active = models.BooleanField(default=True)
    rate_limit_per_minute = models.IntegerField(default=120)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"


class WebhookEndpoint(models.Model):
    name = models.CharField(max_length=150)
    target_url = models.URLField()
    secret_token = models.CharField(max_length=64, default=secrets.token_hex)
    is_active = models.BooleanField(default=True)
    events_subscribed = models.TextField(default="employee.created,leave.approved,attendance.punch,payroll.disbursed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook: {self.name} -> {self.target_url}"


class BiometricDeviceLog(models.Model):
    device_id = models.CharField(max_length=50, default="ZKTECO-GATE-01")
    biometric_user_id = models.CharField(max_length=50)
    punch_timestamp = models.DateTimeField(default=timezone.now)
    punch_type = models.CharField(max_length=20, choices=[('IN', 'Punch In'), ('OUT', 'Punch Out')], default='IN')
    is_synced = models.BooleanField(default=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Biometric Punch: {self.biometric_user_id} @ {self.punch_timestamp}"
""")

write_file("apps/api/views.py", """
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.employees.models import Employee
from apps.attendance.models import AttendanceRecord
from apps.projects.models import Project
from apps.api.models import APIKey, WebhookEndpoint, BiometricDeviceLog

@login_required
def api_documentation_portal(request):
    api_keys = APIKey.objects.filter(user=request.user)
    webhooks = WebhookEndpoint.objects.filter(is_active=True)
    endpoints = [
        {'method': 'GET', 'path': '/api/v1/employees/', 'desc': 'List all active employees with pagination and filters'},
        {'method': 'GET', 'path': '/api/v1/attendance/today/', 'desc': 'Get live daily workforce presence statistics'},
        {'method': 'POST', 'path': '/api/v1/biometric/sync/', 'desc': 'Ingest fingerprint/facial biometric gate punches'},
        {'method': 'GET', 'path': '/api/v1/projects/', 'desc': 'List all active enterprise projects and completion %'},
    ]
    return render(request, 'api/documentation.html', {'api_keys': api_keys, 'webhooks': webhooks, 'endpoints': endpoints})

def api_employees_list(request):
    employees = Employee.objects.filter(is_active=True).select_related('department', 'designation')[:50]
    data = []
    for emp in employees:
        data.append({
            'id': emp.id,
            'employee_id': emp.employee_id,
            'full_name': emp.full_name,
            'email': emp.user.email if emp.user else '',
            'department': emp.department.name if emp.department else None,
            'designation': emp.designation.title if emp.designation else None,
            'joining_date': str(emp.joining_date),
            'status': emp.employment_status,
        })
    return JsonResponse({'count': len(data), 'results': data})

def api_attendance_today(request):
    today_records = AttendanceRecord.objects.select_related('employee')[:50]
    data = []
    for r in today_records:
        data.append({
            'employee': r.employee.full_name,
            'date': str(r.date),
            'status': r.status,
            'check_in': str(r.check_in_time) if r.check_in_time else None,
            'check_out': str(r.check_out_time) if r.check_out_time else None,
        })
    return JsonResponse({'count': len(data), 'records': data})

@csrf_exempt
def api_biometric_sync(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            log = BiometricDeviceLog.objects.create(
                device_id=body.get('device_id', 'ZKTECO-GATE-01'),
                biometric_user_id=body.get('user_id', 'EMP-1001'),
                punch_type=body.get('punch_type', 'IN'),
            )
            return JsonResponse({'status': 'success', 'log_id': log.id, 'message': 'Biometric punch recorded'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

def api_projects_list(request):
    projects = Project.objects.all()[:50]
    data = [{'id': p.id, 'name': p.name, 'code': p.code, 'status': p.status, 'progress_percentage': p.progress_percentage} for p in projects]
    return JsonResponse({'count': len(data), 'projects': data})
""")

write_file("apps/api/urls.py", """
from django.urls import path
from apps.api import views

app_name = 'api'

urlpatterns = [
    path('docs/', views.api_documentation_portal, name='docs'),
    path('v1/employees/', views.api_employees_list, name='api_employees'),
    path('v1/attendance/today/', views.api_attendance_today, name='api_attendance_today'),
    path('v1/biometric/sync/', views.api_biometric_sync, name='api_biometric_sync'),
    path('v1/projects/', views.api_projects_list, name='api_projects'),
]
""")

write_file("apps/api/admin.py", """
from django.contrib import admin
from apps.api.models import APIKey, WebhookEndpoint, BiometricDeviceLog

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'rate_limit_per_minute', 'created_at')

@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_url', 'is_active')

@admin.register(BiometricDeviceLog)
class BiometricDeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'biometric_user_id', 'punch_timestamp', 'punch_type', 'is_synced')
""")

# ==============================================================================
# 10. APPS / AUTOMATION (Event-Driven Workflow Builder)
# ==============================================================================

write_file("apps/automation/__init__.py", """default_app_config = 'apps.automation.apps.AutomationConfig'""")

write_file("apps/automation/apps.py", """
from django.apps import AppConfig

class AutomationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.automation'
    verbose_name = 'Smart Workflow Automation & Event-Action Triggers'
""")

write_file("apps/automation/models.py", """
from django.db import models
from django.conf import settings
from django.utils import timezone

class AutomationRule(models.Model):
    TRIGGER_EVENTS = [
        ('EMPLOYEE_JOINED', 'When a new employee joins (Onboarding)'),
        ('LEAVE_APPROVED', 'When a leave request is approved'),
        ('PROBATION_DUE', 'When employee probation review date arrives'),
        ('WORK_ANNIVERSARY', 'On employee work anniversary milestone'),
        ('BIRTHDAY_ALERT', 'On employee birthday'),
        ('EXPENSE_SUBMITTED', 'When high-value expense claim is filed'),
        ('PAYROLL_PROCESSED', 'When monthly payroll run is completed'),
    ]

    ACTION_TYPES = [
        ('DISPATCH_EMAIL', 'Dispatch Automated Notification Email'),
        ('SEND_IN_APP_ALERT', 'Send Instant In-App System Alert'),
        ('CREATE_TASK', 'Create Follow-up Task for Manager'),
        ('TRIGGER_WEBHOOK', 'Fire Webhook to External ERP / Slack'),
        ('AWARD_KUDOS_BADGE', 'Award Automated Recognition Badge'),
    ]

    name = models.CharField(max_length=200, help_text="e.g. Auto-Welcome Email & Task Generation on Hire")
    trigger_event = models.CharField(max_length=50, choices=TRIGGER_EVENTS)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    action_payload = models.TextField(help_text="JSON or configuration parameters for the action")
    is_active = models.BooleanField(default=True)
    total_executions = models.IntegerField(default=0)
    last_executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rule: {self.name} [{self.get_trigger_event_display()}]"


class ExecutionLog(models.Model):
    rule = models.ForeignKey(AutomationRule, on_delete=models.CASCADE, related_name='execution_logs')
    executed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Executed Successfully'), ('FAILED', 'Execution Error'), ('SKIPPED', 'Conditions Not Met')], default='SUCCESS')
    details = models.TextField()

    class Meta:
        ordering = ['-executed_at']

    def __str__(self):
        return f"Log: {self.rule.name} @ {self.executed_at} ({self.status})"
""")

write_file("apps/automation/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.automation.models import AutomationRule, ExecutionLog

@login_required
def automation_dashboard(request):
    rules = AutomationRule.objects.all()
    logs = ExecutionLog.objects.select_related('rule')[:15]
    active_count = rules.filter(is_active=True).count()
    total_runs = sum(r.total_executions for r in rules)

    context = {
        'rules': rules,
        'logs': logs,
        'active_count': active_count,
        'total_runs': total_runs,
    }
    return render(request, 'automation/dashboard.html', context)

@login_required
def trigger_rule_simulation(request, pk):
    rule = get_object_or_404(AutomationRule, pk=pk)
    rule.total_executions += 1
    rule.save()
    ExecutionLog.objects.create(
        rule=rule,
        status='SUCCESS',
        details=f"Automated workflow trigger simulation succeeded for rule '{rule.name}' with event {rule.trigger_event}."
    )
    messages.success(request, f"Rule '{rule.name}' executed successfully!")
    return redirect('automation:dashboard')
""")

write_file("apps/automation/urls.py", """
from django.urls import path
from apps.automation import views

app_name = 'automation'

urlpatterns = [
    path('', views.automation_dashboard, name='dashboard'),
    path('rules/<int:pk>/trigger/', views.trigger_rule_simulation, name='trigger_rule'),
]
""")

write_file("apps/automation/admin.py", """
from django.contrib import admin
from apps.automation.models import AutomationRule, ExecutionLog

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'trigger_event', 'action_type', 'is_active', 'total_executions')

@admin.register(ExecutionLog)
class ExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('rule', 'executed_at', 'status')
    list_filter = ('status',)
""")

print("Finished Timesheets, Surveys, Workplace, API, and Automation module generation.")
