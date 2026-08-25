"""
URL configuration for Smart Employee Management System.
Maps all 24 functional modules cleanly with role-based routing.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return redirect('authentication:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),

    # Group 1: Core & Security
    path('auth/', include(('apps.authentication.urls', 'authentication'), namespace='authentication')),
    path('employees/', include(('apps.employees.urls', 'employees'), namespace='employees')),
    path('organization/', include(('apps.organization.urls', 'organization'), namespace='organization')),
    path('permissions/', include(('apps.permissions.urls', 'permissions'), namespace='permissions')),

    # Group 2: Time & Workforce
    path('attendance/', include(('apps.attendance.urls', 'attendance'), namespace='attendance')),
    path('leave/', include(('apps.leave_management.urls', 'leave_management'), namespace='leave_management')),
    path('shifts/', include(('apps.shifts.urls', 'shifts'), namespace='shifts')),
    path('workload/', include(('apps.workload.urls', 'workload'), namespace='workload')),

    # Group 3: Work & Productivity
    path('projects/', include(('apps.projects.urls', 'projects'), namespace='projects')),
    path('tasks/', include(('apps.tasks.urls', 'tasks'), namespace='tasks')),
    path('skills/', include(('apps.skills.urls', 'skills'), namespace='skills')),
    path('goals/', include(('apps.goals.urls', 'goals'), namespace='goals')),

    # Group 4: Employee Development
    path('performance/', include(('apps.performance.urls', 'performance'), namespace='performance')),
    path('training/', include(('apps.training.urls', 'training'), namespace='training')),
    path('recognition/', include(('apps.recognition.urls', 'recognition'), namespace='recognition')),

    # Group 5: Employee Services
    path('assets/', include(('apps.assets.urls', 'assets'), namespace='assets')),
    path('expenses/', include(('apps.expenses.urls', 'expenses'), namespace='expenses')),
    path('helpdesk/', include(('apps.helpdesk.urls', 'helpdesk'), namespace='helpdesk')),
    path('documents/', include(('apps.documents.urls', 'documents'), namespace='documents')),
    path('announcements/', include(('apps.announcements.urls', 'announcements'), namespace='announcements')),
    path('notifications/', include(('apps.notifications.urls', 'notifications'), namespace='notifications')),

    # Group 6: Intelligence & Administration
    path('insights/', include(('apps.insights.urls', 'insights'), namespace='insights')),
    path('reports/', include(('apps.reports.urls', 'reports'), namespace='reports')),
    path('administration/', include(('apps.administration.urls', 'administration'), namespace='administration')),

    # Group 7: Compensation, Talent & Lifecycle (Enterprise Expansion)
    path('payroll/', include(('apps.payroll.urls', 'payroll'), namespace='payroll')),
    path('recruitment/', include(('apps.recruitment.urls', 'recruitment'), namespace='recruitment')),
    path('lifecycle/', include(('apps.lifecycle.urls', 'lifecycle'), namespace='lifecycle')),
    path('compliance/', include(('apps.compliance.urls', 'compliance'), namespace='compliance')),
    path('benefits/', include(('apps.benefits.urls', 'benefits'), namespace='benefits')),
    path('timesheets/', include(('apps.timesheets.urls', 'timesheets'), namespace='timesheets')),
    path('surveys/', include(('apps.surveys.urls', 'surveys'), namespace='surveys')),
    path('workplace/', include(('apps.workplace.urls', 'workplace'), namespace='workplace')),
    path('api/', include(('apps.api.urls', 'api'), namespace='api')),
    path('automation/', include(('apps.automation.urls', 'automation'), namespace='automation')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
