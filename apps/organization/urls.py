from django.urls import path

from apps.organization import views

app_name = 'organization'

urlpatterns = [
    path('profile/', views.organization_profile_view, name='profile'),
    path('chart/', views.org_chart_view, name='org_chart'),
    
    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:dept_id>/update/', views.department_update, name='department_update'),

    # Teams
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:team_id>/update/', views.team_update, name='team_update'),

    # Designations
    path('designations/', views.designation_list, name='designation_list'),
    path('designations/create/', views.designation_create, name='designation_create'),
    path('designations/<int:desig_id>/update/', views.designation_update, name='designation_update'),
]
