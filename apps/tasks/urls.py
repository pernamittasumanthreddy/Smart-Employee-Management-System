from django.urls import path

from apps.tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('kanban/', views.my_tasks_kanban, name='my_tasks_kanban'),
    path('create/', views.task_create_view, name='task_create'),
    path('<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('<int:task_id>/update-status/', views.task_update_status, name='update_status'),
    path('<int:task_id>/comments/add/', views.task_add_comment, name='add_comment'),
    path('<int:task_id>/subtasks/add/', views.task_add_subtask, name='add_subtask'),
    path('subtasks/<int:subtask_id>/toggle/', views.task_toggle_subtask, name='toggle_subtask'),
]
