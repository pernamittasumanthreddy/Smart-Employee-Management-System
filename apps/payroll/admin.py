from django.contrib import admin
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip, TaxDeclaration

@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'annual_ctc', 'currency', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active', 'currency')

@admin.register(EmployeeSalaryAssignment)
class EmployeeSalaryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary_structure', 'effective_from', 'bank_name', 'tax_regime')
    search_fields = ('employee__user__first_name', 'employee__employee_id', 'pan_number')

@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ('title', 'payroll_month', 'payroll_year', 'status', 'total_employees', 'total_net_pay', 'payment_date')
    list_filter = ('status', 'payroll_year')

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll_run', 'gross_earnings', 'total_deductions', 'net_salary')
    search_fields = ('employee__user__first_name', 'employee__employee_id')

@admin.register(TaxDeclaration)
class TaxDeclarationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'financial_year', 'regime', 'status')
    list_filter = ('regime', 'status', 'financial_year')
