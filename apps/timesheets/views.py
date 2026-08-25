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
