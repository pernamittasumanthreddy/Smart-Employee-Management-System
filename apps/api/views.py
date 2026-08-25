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
    employees = Employee.objects.select_related('department', 'designation')[:50]
    data = []
    for emp in employees:
        data.append({
            'id': emp.id,
            'employee_id': emp.employee_id,
            'full_name': emp.full_name,
            'email': emp.user.email if emp.user else '',
            'department': emp.department.name if emp.department else None,
            'designation': emp.designation.title if emp.designation else None,
            'joining_date': str(emp.date_of_joining) if hasattr(emp, 'date_of_joining') else '',
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
