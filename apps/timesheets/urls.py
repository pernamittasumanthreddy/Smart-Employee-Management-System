from django.urls import path
from apps.timesheets import views

app_name = 'timesheets'

urlpatterns = [
    path('', views.timesheets_dashboard, name='dashboard'),
    path('<int:pk>/', views.timesheet_detail, name='timesheet_detail'),
    path('<int:pk>/approve/', views.timesheet_approval, name='timesheet_approval'),
]
