from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.employees.models import Employee

class InsurancePolicy(models.Model):
    POLICY_TYPES = [('GMC', 'Group Mediclaim Policy (Family Floater)'), ('GPA', 'Group Personal Accident'), ('GTL', 'Group Term Life Insurance')]

    name = models.CharField(max_length=200, help_text="e.g. Star Health Corporate Floater 5L")
    policy_number = models.CharField(max_length=100, unique=True)
    provider_name = models.CharField(max_length=150, default="ICICI Lombard / Star Health")
    policy_type = models.CharField(max_length=30, choices=POLICY_TYPES, default='GMC')
    sum_insured = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('500000.00'))
    start_date = models.DateField()
    end_date = models.DateField()
    tpa_name = models.CharField(max_length=150, default="Medi Assist TPA Services", help_text="Third Party Administrator")
    tpa_toll_free = models.CharField(max_length=50, default="1800-425-9449")
    cashless_hospitals_count = models.IntegerField(default=12000)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Coverage: INR {self.sum_insured:,.0f})"


class EmployeeInsuranceEnrollment(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='insurance_enrollment')
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='enrollments')
    card_number = models.CharField(max_length=50, unique=True)
    enrolled_date = models.DateField(default=timezone.now)
    sum_insured_allocated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('500000.00'))
    total_claims_utilized = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Insurance: {self.employee.full_name} ({self.card_number})"

    @property
    def remaining_coverage(self):
        return self.sum_insured_allocated - self.total_claims_utilized


class InsuranceDependent(models.Model):
    RELATION_CHOICES = [('SPOUSE', 'Spouse / Partner'), ('CHILD_1', 'Child 1'), ('CHILD_2', 'Child 2'), ('PARENT_1', 'Father / Mother-in-Law'), ('PARENT_2', 'Mother / Father-in-Law')]

    enrollment = models.ForeignKey(EmployeeInsuranceEnrollment, on_delete=models.CASCADE, related_name='dependents')
    full_name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=30, choices=RELATION_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')])
    health_card_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_relationship_display()}) - {self.enrollment.employee.full_name}"


class InsuranceClaim(models.Model):
    STATUS_CHOICES = [('SUBMITTED', 'Submitted to TPA'), ('UNDER_REVIEW', 'Under Document Verification'), ('APPROVED', 'Approved for Cashless/Reimbursement'), ('SETTLED', 'Claim Amount Settled & Paid'), ('REJECTED', 'Claim Rejected by Insurer')]

    enrollment = models.ForeignKey(EmployeeInsuranceEnrollment, on_delete=models.CASCADE, related_name='claims')
    claim_id = models.CharField(max_length=50, unique=True)
    patient_name = models.CharField(max_length=150)
    hospital_name = models.CharField(max_length=200)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    diagnosis = models.CharField(max_length=255, blank=True, default='General Medical Care')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED')
    settled_date = models.DateField(null=True, blank=True)
    tpa_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        if 'claim_number' in kwargs and 'claim_id' not in kwargs:
            kwargs['claim_id'] = kwargs.pop('claim_number')
        kwargs.pop('relationship', None)
        if 'diagnosis' not in kwargs:
            kwargs['diagnosis'] = 'General Medical Care'
        super().__init__(*args, **kwargs)


    @property
    def claim_number(self):
        return self.claim_id

    @claim_number.setter
    def claim_number(self, val):
        self.claim_id = val

    def __str__(self):
        return f"Claim #{self.claim_id} - {self.patient_name} (INR {self.claimed_amount:,.2f})"



class FlexibleBenefitPlan(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='fbp_plan')
    financial_year = models.CharField(max_length=20, default="2026-2027")
    total_fbp_budget = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('120000.00'))
    meal_card_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('26400.00'))
    fuel_driver_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('30000.00'))
    books_periodicals = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('15000.00'))
    internet_telecom = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('24000.00'))
    gym_wellness_reimbursement = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('24600.00'))
    is_locked = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FBP: {self.employee.full_name} FY {self.financial_year}"
