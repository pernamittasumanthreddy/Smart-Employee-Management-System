from django.urls import path
from apps.payroll import views

app_name = 'payroll'

urlpatterns = [
    path('', views.payroll_dashboard, name='dashboard'),
    path('structures/', views.salary_structure_list, name='structure_list'),
    path('structures/create/', views.salary_structure_create, name='structure_create'),
    path('runs/', views.payroll_run_list, name='run_list'),
    path('runs/<int:pk>/', views.payroll_run_detail, name='run_detail'),
    path('runs/<int:pk>/process/', views.payroll_run_process, name='run_process'),
    path('my-payslips/', views.my_payslips, name='my_payslips'),
    path('payslip/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('tax-declaration/', views.tax_declaration_portal, name='tax_declaration'),
]
