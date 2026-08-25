from django.urls import path

from apps.projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='project_list'),
    path('create/', views.project_create_view, name='project_create'),
    path('<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('<int:project_id>/update/', views.project_update_view, name='project_update'),
    path('<int:project_id>/milestones/add/', views.project_add_milestone, name='add_milestone'),
    path('milestones/<int:milestone_id>/toggle/', views.project_toggle_milestone, name='toggle_milestone'),
]
