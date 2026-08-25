from django.urls import path
from apps.compliance import views

app_name = 'compliance'

urlpatterns = [
    path('', views.compliance_dashboard, name='dashboard'),
    path('registers/', views.register_list, name='register_list'),
    path('audits/', views.audit_list, name='audit_list'),
    path('posh/', views.posh_portal, name='posh_portal'),
]
