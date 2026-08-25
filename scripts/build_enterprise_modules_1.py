import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\EMS")

def write_file(rel_path, content):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path} ({len(content.splitlines())} lines)")

# ==============================================================================
# 1. APPS / PAYROLL
# ==============================================================================

write_file("apps/payroll/__init__.py", """default_app_config = 'apps.payroll.apps.PayrollConfig'""")

write_file("apps/payroll/apps.py", """
from django.apps import AppConfig

class PayrollConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.payroll'
    verbose_name = 'Enterprise Payroll & Statutory Compensation'
""")

write_file("apps/payroll/models.py", """
import decimal
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class SalaryStructure(models.Model):
    name = models.CharField(max_length=150, unique=True, help_text="e.g. Executive Engineering Grade A, Standard Staff L2")
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    currency = models.CharField(max_length=10, default="INR")
    annual_ctc = models.DecimalField(max_digits=12, decimal_places=2, help_text="Cost to Company per annum")
    basic_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('40.00'), help_text="Percentage of CTC as Basic Pay")
    hra_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('20.00'), help_text="Percentage of Basic as House Rent Allowance")
    da_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'), help_text="Dearness Allowance percentage")
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1250.00'))
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1600.00'))
    pf_employee_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('12.00'), help_text="Provident Fund employee deduction %")
    pf_employer_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('12.00'), help_text="Provident Fund employer contribution %")
    esi_employee_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.75'), help_text="ESI Employee %")
    esi_employer_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('3.25'), help_text="ESI Employer %")
    professional_tax = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('200.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-annual_ctc']
        verbose_name = 'Salary Structure'
        verbose_name_plural = 'Salary Structures'

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.currency} {self.annual_ctc:,.2f}"

    @property
    def monthly_ctc(self):
        return (self.annual_ctc / Decimal('12.0')).quantize(Decimal('0.01'))

    @property
    def monthly_basic(self):
        return (self.monthly_ctc * (self.basic_percentage / Decimal('100.0'))).quantize(Decimal('0.01'))

    @property
    def monthly_hra(self):
        return (self.monthly_basic * (self.hra_percentage / Decimal('100.0'))).quantize(Decimal('0.01'))

    @property
    def monthly_da(self):
        return (self.monthly_basic * (self.da_percentage / Decimal('100.0'))).quantize(Decimal('0.01'))

    @property
    def monthly_pf_employee(self):
        return (self.monthly_basic * (self.pf_employee_rate / Decimal('100.0'))).quantize(Decimal('0.01'))

    @property
    def monthly_gross(self):
        return self.monthly_basic + self.monthly_hra + self.monthly_da + self.special_allowance + self.medical_allowance + self.conveyance_allowance

    @property
    def monthly_deductions(self):
        return self.monthly_pf_employee + self.professional_tax

    @property
    def monthly_net_pay(self):
        return self.monthly_gross - self.monthly_deductions


class EmployeeSalaryAssignment(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_assignment')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.PROTECT, related_name='assignments')
    effective_from = models.DateField(default=timezone.now)
    bank_name = models.CharField(max_length=150, default="State Bank of India")
    bank_account_number = models.CharField(max_length=50, default="987654321012")
    bank_ifsc_code = models.CharField(max_length=20, default="SBIN0001234")
    pan_number = models.CharField(max_length=20, default="ABCDE1234F")
    uan_number = models.CharField(max_length=30, blank=True, help_text="Universal Account Number for PF")
    tax_regime = models.CharField(max_length=20, choices=[('NEW', 'New Tax Regime (Sec 115BAC)'), ('OLD', 'Old Tax Regime (With Exemptions)')], default='NEW')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Employee Salary Assignment'
        verbose_name_plural = 'Employee Salary Assignments'

    def __str__(self):
        return f"{self.employee.full_name} - {self.salary_structure.name}"


class PayrollRun(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft / Calculating'),
        ('REVIEW', 'Under HR & Finance Review'),
        ('APPROVED', 'Approved by CFO / Leadership'),
        ('DISBURSED', 'Disbursed / Paid'),
        ('LOCKED', 'Locked & Archived'),
    ]

    title = models.CharField(max_length=200, help_text="e.g. Payroll Run - August 2026")
    payroll_month = models.IntegerField(default=8)
    payroll_year = models.IntegerField(default=2026)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    total_employees = models.IntegerField(default=0)
    total_gross_pay = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_deductions = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_net_pay = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_employer_pf = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_employer_esi = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payrolls')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payroll_year', '-payroll_month']
        unique_together = ('payroll_year', 'payroll_month')
        verbose_name = 'Payroll Run'
        verbose_name_plural = 'Payroll Runs'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Payslip(models.Model):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.PROTECT)
    
    # Working Days Summary
    total_working_days = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('30.00'))
    days_present = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('28.00'))
    days_paid_leave = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('2.00'))
    days_lop = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), help_text="Loss of Pay Days")

    # Earnings
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    da = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    performance_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    gross_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # Deductions
    pf_employee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    esi_employee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    income_tax_tds = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    lop_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    # Net
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    net_salary_in_words = models.CharField(max_length=255, blank=True)

    # Employer Contributions (CTC part)
    pf_employer = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    esi_employer = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    gratuity_accrual = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    payment_mode = models.CharField(max_length=30, default="Direct Bank Transfer (NEFT)")
    transaction_reference = models.CharField(max_length=100, blank=True)
    is_published_to_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('payroll_run', 'employee')
        ordering = ['employee__user__first_name', 'employee__employee_id']
        verbose_name = 'Payslip'
        verbose_name_plural = 'Payslips'

    def __str__(self):
        return f"Payslip: {self.employee.full_name} ({self.payroll_run.title})"


class TaxDeclaration(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tax_declarations')
    financial_year = models.CharField(max_length=20, default="2026-2027")
    regime = models.CharField(max_length=20, choices=[('NEW', 'New Regime'), ('OLD', 'Old Regime')], default='NEW')
    
    # Section 80C
    section_80c_lic = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    section_80c_ppf = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    section_80c_elss = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    section_80c_tuition = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Section 80D Mediclaim
    section_80d_self = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    section_80d_parents = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Section 24 Home Loan Interest
    home_loan_interest = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    house_rent_paid_annual = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Section 80CCD NPS
    nps_additional = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    status = models.CharField(max_length=20, choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('VERIFIED', 'Verified by HR/Finance'), ('REJECTED', 'Needs Revision')], default='DRAFT')
    hr_reviewer_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'financial_year')
        verbose_name = 'Tax Declaration'
        verbose_name_plural = 'Tax Declarations'

    def __str__(self):
        return f"Tax Declaration: {self.employee.full_name} FY {self.financial_year}"
""")

write_file("apps/payroll/services.py", """
from decimal import Decimal
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip, TaxDeclaration
from apps.employees.models import Employee

class PayrollCalculationService:
    @staticmethod
    def calculate_employee_monthly_salary(employee, payroll_run, days_present=28, days_paid_leave=2, days_lop=0, bonus=0, overtime=0):
        try:
            assignment = employee.salary_assignment
            structure = assignment.salary_structure
        except Exception:
            structure = SalaryStructure.objects.first()
            if not structure:
                structure = SalaryStructure.objects.create(
                    name="Default Corporate Grade",
                    code="CORP-L1",
                    annual_ctc=Decimal('600000.00'),
                    basic_percentage=Decimal('40.00'),
                    hra_percentage=Decimal('20.00')
                )

        monthly_basic = structure.monthly_basic
        monthly_hra = structure.monthly_hra
        monthly_da = structure.monthly_da
        special_allowance = structure.special_allowance
        conveyance = structure.conveyance_allowance
        medical = structure.medical_allowance
        bonus_dec = Decimal(str(bonus))
        overtime_dec = Decimal(str(overtime))

        total_gross = monthly_basic + monthly_hra + monthly_da + special_allowance + conveyance + medical + bonus_dec + overtime_dec

        # Deductions
        pf_emp = structure.monthly_pf_employee
        esi_emp = structure.monthly_gross * (structure.esi_employee_rate / Decimal('100.0')) if total_gross <= Decimal('21000.00') else Decimal('0.00')
        pt = structure.professional_tax
        lop_ded = (total_gross / Decimal('30.00')) * Decimal(str(days_lop))
        
        # Approximate TDS estimation
        annual_est = total_gross * Decimal('12.0')
        tds_monthly = Decimal('0.00')
        if annual_est > Decimal('700000.00'):
            taxable = annual_est - Decimal('700000.00')
            tds_monthly = ((taxable * Decimal('0.10')) / Decimal('12.0')).quantize(Decimal('0.01'))

        total_ded = pf_emp + esi_emp + pt + lop_ded + tds_monthly
        net_pay = total_gross - total_ded

        # Employer contributions
        pf_empr = structure.monthly_basic * (structure.pf_employer_rate / Decimal('100.0'))
        esi_empr = structure.monthly_gross * (structure.esi_employer_rate / Decimal('100.0')) if total_gross <= Decimal('21000.00') else Decimal('0.00')
        gratuity = (monthly_basic * Decimal('15') / Decimal('26')) / Decimal('12.0')

        return {
            'structure': structure,
            'basic_pay': monthly_basic.quantize(Decimal('0.01')),
            'hra': monthly_hra.quantize(Decimal('0.01')),
            'da': monthly_da.quantize(Decimal('0.01')),
            'special_allowance': special_allowance.quantize(Decimal('0.01')),
            'conveyance_allowance': conveyance.quantize(Decimal('0.01')),
            'medical_allowance': medical.quantize(Decimal('0.01')),
            'performance_bonus': bonus_dec.quantize(Decimal('0.01')),
            'overtime_pay': overtime_dec.quantize(Decimal('0.01')),
            'gross_earnings': total_gross.quantize(Decimal('0.01')),
            'pf_employee': pf_emp.quantize(Decimal('0.01')),
            'esi_employee': esi_emp.quantize(Decimal('0.01')),
            'professional_tax': pt.quantize(Decimal('0.01')),
            'income_tax_tds': tds_monthly.quantize(Decimal('0.01')),
            'lop_deduction': lop_ded.quantize(Decimal('0.01')),
            'total_deductions': total_ded.quantize(Decimal('0.01')),
            'net_salary': net_pay.quantize(Decimal('0.01')),
            'pf_employer': pf_empr.quantize(Decimal('0.01')),
            'esi_employer': esi_empr.quantize(Decimal('0.01')),
            'gratuity_accrual': gratuity.quantize(Decimal('0.01')),
        }

    @classmethod
    def execute_payroll_run(cls, payroll_run, user=None):
        employees = Employee.objects.filter(is_active=True)
        total_gross = Decimal('0.00')
        total_ded = Decimal('0.00')
        total_net = Decimal('0.00')
        total_pf = Decimal('0.00')
        total_esi = Decimal('0.00')
        count = 0

        for emp in employees:
            calc = cls.calculate_employee_monthly_salary(emp, payroll_run)
            payslip, _ = Payslip.objects.update_or_create(
                payroll_run=payroll_run,
                employee=emp,
                defaults={
                    'salary_structure': calc['structure'],
                    'total_working_days': Decimal('30.00'),
                    'days_present': Decimal('28.00'),
                    'days_paid_leave': Decimal('2.00'),
                    'days_lop': Decimal('0.00'),
                    'basic_pay': calc['basic_pay'],
                    'hra': calc['hra'],
                    'da': calc['da'],
                    'special_allowance': calc['special_allowance'],
                    'conveyance_allowance': calc['conveyance_allowance'],
                    'medical_allowance': calc['medical_allowance'],
                    'performance_bonus': calc['performance_bonus'],
                    'overtime_pay': calc['overtime_pay'],
                    'gross_earnings': calc['gross_earnings'],
                    'pf_employee': calc['pf_employee'],
                    'esi_employee': calc['esi_employee'],
                    'professional_tax': calc['professional_tax'],
                    'income_tax_tds': calc['income_tax_tds'],
                    'lop_deduction': calc['lop_deduction'],
                    'total_deductions': calc['total_deductions'],
                    'net_salary': calc['net_salary'],
                    'pf_employer': calc['pf_employer'],
                    'esi_employer': calc['esi_employer'],
                    'gratuity_accrual': calc['gratuity_accrual'],
                    'is_published_to_employee': True,
                }
            )
            total_gross += calc['gross_earnings']
            total_ded += calc['total_deductions']
            total_net += calc['net_salary']
            total_pf += (calc['pf_employee'] + calc['pf_employer'])
            total_esi += (calc['esi_employee'] + calc['esi_employer'])
            count += 1

        payroll_run.total_employees = count
        payroll_run.total_gross_pay = total_gross
        payroll_run.total_deductions = total_ded
        payroll_run.total_net_pay = total_net
        payroll_run.total_employer_pf = total_pf
        payroll_run.total_employer_esi = total_esi
        payroll_run.status = 'APPROVED'
        if user:
            payroll_run.processed_by = user
        payroll_run.save()
        return payroll_run
""")

write_file("apps/payroll/forms.py", """
from django import forms
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, TaxDeclaration

class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_ctc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'basic_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'hra_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'da_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'special_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'medical_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'conveyance_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pf_employee_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pf_employer_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'professional_tax': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PayrollRunForm(forms.ModelForm):
    class Meta:
        model = PayrollRun
        fields = ['title', 'payroll_month', 'payroll_year', 'start_date', 'end_date', 'payment_date', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'payroll_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'payroll_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TaxDeclarationForm(forms.ModelForm):
    class Meta:
        model = TaxDeclaration
        exclude = ['employee', 'status', 'hr_reviewer_comments']
        widgets = {
            'financial_year': forms.TextInput(attrs={'class': 'form-control'}),
            'regime': forms.Select(attrs={'class': 'form-select'}),
            'section_80c_lic': forms.NumberInput(attrs={'class': 'form-control'}),
            'section_80c_ppf': forms.NumberInput(attrs={'class': 'form-control'}),
            'section_80c_elss': forms.NumberInput(attrs={'class': 'form-control'}),
            'section_80c_tuition': forms.NumberInput(attrs={'class': 'form-control'}),
            'section_80d_self': forms.NumberInput(attrs={'class': 'form-control'}),
            'section_80d_parents': forms.NumberInput(attrs={'class': 'form-control'}),
            'home_loan_interest': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_rent_paid_annual': forms.NumberInput(attrs={'class': 'form-control'}),
            'nps_additional': forms.NumberInput(attrs={'class': 'form-control'}),
        }
""")

write_file("apps/payroll/views.py", """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.http import HttpResponse
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip, TaxDeclaration
from apps.payroll.forms import SalaryStructureForm, PayrollRunForm, TaxDeclarationForm
from apps.payroll.services import PayrollCalculationService

@login_required
def payroll_dashboard(request):
    runs = PayrollRun.objects.all()[:6]
    structures = SalaryStructure.objects.filter(is_active=True)
    total_annual_payroll = structures.aggregate(total=Sum('annual_ctc'))['total'] or 0
    recent_payslips = Payslip.objects.select_related('employee', 'payroll_run')[:10]
    
    # User's personal latest payslip
    user_payslip = None
    if hasattr(request.user, 'employee_profile'):
        user_payslip = Payslip.objects.filter(employee=request.user.employee_profile).order_by('-payroll_run__payroll_year', '-payroll_run__payroll_month').first()

    context = {
        'runs': runs,
        'structures': structures,
        'total_annual_payroll': total_annual_payroll,
        'recent_payslips': recent_payslips,
        'user_payslip': user_payslip,
    }
    return render(request, 'payroll/dashboard.html', context)

@login_required
def salary_structure_list(request):
    structures = SalaryStructure.objects.all()
    return render(request, 'payroll/structure_list.html', {'structures': structures})

@login_required
def salary_structure_create(request):
    if request.method == 'POST':
        form = SalaryStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary structure configured successfully.")
            return redirect('payroll:structure_list')
    else:
        form = SalaryStructureForm()
    return render(request, 'payroll/structure_form.html', {'form': form, 'title': 'Create Salary Structure'})

@login_required
def payroll_run_list(request):
    runs = PayrollRun.objects.all()
    return render(request, 'payroll/run_list.html', {'runs': runs})

@login_required
def payroll_run_detail(request, pk):
    run = get_object_or_404(PayrollRun, pk=pk)
    payslips = run.payslips.select_related('employee__user', 'employee__department').all()
    return render(request, 'payroll/run_detail.html', {'run': run, 'payslips': payslips})

@login_required
def payroll_run_process(request, pk):
    run = get_object_or_404(PayrollRun, pk=pk)
    PayrollCalculationService.execute_payroll_run(run, request.user)
    messages.success(request, f"Payroll for {run.title} calculated and disbursed successfully!")
    return redirect('payroll:run_detail', pk=run.pk)

@login_required
def my_payslips(request):
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, "Employee profile not found.")
        return redirect('payroll:dashboard')
    payslips = Payslip.objects.filter(employee=request.user.employee_profile).select_related('payroll_run')
    return render(request, 'payroll/my_payslips.html', {'payslips': payslips})

@login_required
def payslip_detail(request, pk):
    payslip = get_object_or_404(Payslip.objects.select_related('employee', 'payroll_run', 'salary_structure'), pk=pk)
    return render(request, 'payroll/payslip_view.html', {'payslip': payslip})

@login_required
def tax_declaration_portal(request):
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, "Employee profile required.")
        return redirect('payroll:dashboard')
    dec, created = TaxDeclaration.objects.get_or_create(
        employee=request.user.employee_profile,
        financial_year="2026-2027"
    )
    if request.method == 'POST':
        form = TaxDeclarationForm(request.POST, instance=dec)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 'SUBMITTED'
            obj.save()
            messages.success(request, "Tax exemptions declaration submitted successfully for verification.")
            return redirect('payroll:tax_declaration')
    else:
        form = TaxDeclarationForm(instance=dec)
    return render(request, 'payroll/tax_declaration.html', {'form': form, 'declaration': dec})
""")

write_file("apps/payroll/urls.py", """
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
""")

write_file("apps/payroll/admin.py", """
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
""")

print("Finished Payroll module generation.")
