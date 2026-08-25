from django.urls import path

from apps.employees import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('directory/', views.employee_directory, name='directory'),
    path('self/', views.employee_self_profile, name='self_profile'),
    path('create/', views.employee_create, name='employee_create'),
    path('export/', views.employee_export_csv, name='employee_export'),
    path('<int:employee_id>/360/', views.employee_360_view, name='employee_360'),
    path('<int:employee_id>/update/', views.employee_update, name='employee_update'),
]
