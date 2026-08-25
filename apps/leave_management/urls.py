from django.urls import path

from apps.leave_management import views

app_name = 'leave_management'

urlpatterns = [
    path('my-leaves/', views.my_leaves_view, name='my_leaves'),
    path('apply/', views.apply_leave_view, name='apply_leave'),
    path('approvals/', views.leave_approval_list_view, name='approval_list'),
    path('approvals/<int:request_id>/approve/', views.approve_leave_action, name='approve_leave'),
    path('approvals/<int:request_id>/reject/', views.reject_leave_action, name='reject_leave'),
    path('calendar/', views.leave_calendar_view, name='calendar'),
]
