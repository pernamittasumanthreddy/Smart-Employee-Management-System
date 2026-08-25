from django.urls import path

from apps.reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_hub_view, name='hub'),
    path('attendance-leave/', views.attendance_leave_report_view, name='attendance_leave'),
    path('performance/', views.performance_analytics_view, name='performance_analytics'),
    path('project-tasks/', views.project_task_tracking_view, name='project_task_tracking'),
    path('skills-training/', views.skill_training_insights_view, name='skills_training'),
    path('expense-assets/', views.expense_asset_tracking_view, name='expense_assets'),
]
