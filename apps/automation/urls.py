from django.urls import path
from apps.automation import views

app_name = 'automation'

urlpatterns = [
    path('', views.automation_dashboard, name='dashboard'),
    path('rules/<int:pk>/trigger/', views.trigger_rule_simulation, name='trigger_rule'),
]
