import pytest
from decimal import Decimal
from django.utils import timezone
from apps.employees.models import Employee
from apps.payroll.models import SalaryStructure, EmployeeSalaryAssignment, PayrollRun, Payslip
from apps.payroll.services import PayrollCalculationService
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestPayrollCycleE2E:
    def test_monthly_payroll_computation_and_disbursement(self):
        user = User.objects.create_user(username="e2e.payroll.user", password="Password@123")
        emp = Employee.objects.create(
            user=user,
            employee_id="EMP-E2E-PAY-01",
            first_name="Mary",
            last_name="Kom",
            email="mary.pay@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        struct = SalaryStructure.objects.create(
            name="Executive Champion CTC",
            code="BAND-EXEC-01",
            annual_ctc=Decimal('3600000.00'),
            basic_percentage=Decimal('40.00'),
            hra_percentage=Decimal('20.00'),
            da_percentage=Decimal('10.00'),
            special_allowance=Decimal('30000.00'),
            pf_employee_rate=Decimal('12.00'),
            professional_tax=Decimal('200.00')
        )
        EmployeeSalaryAssignment.objects.create(
            employee=emp,
            salary_structure=struct,
            bank_name="HDFC Bank",
            bank_account_number="987654321012",
            pan_number="ABCDE1111G",
            tax_regime="NEW"
        )
        run = PayrollRun.objects.create(
            title="E2E Payroll Execution Cycle",
            payroll_month=8,
            payroll_year=2026,
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        updated = PayrollCalculationService.execute_payroll_run(run)
        assert updated.status == 'APPROVED'
        payslip = Payslip.objects.get(payroll_run=updated, employee=emp)
        assert payslip.net_salary > Decimal('0.00')
