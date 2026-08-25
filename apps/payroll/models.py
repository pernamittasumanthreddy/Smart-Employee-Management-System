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
