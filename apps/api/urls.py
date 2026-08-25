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
