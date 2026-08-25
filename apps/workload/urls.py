from django.urls import path

from apps.workload import views

app_name = 'workload'

urlpatterns = [
    path('', views.workload_dashboard_view, name='dashboard'),
    path('recalculate/', views.recalculate_workload_action, name='recalculate'),
]
