from django.urls import path

from apps.attendance import views

app_name = 'attendance'

urlpatterns = [
    path('punch/', views.punch_in_out_action, name='punch'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),
    path('roster/', views.attendance_roster, name='roster'),
    path('department-summary/', views.department_attendance_summary, name='department_summary'),
]
