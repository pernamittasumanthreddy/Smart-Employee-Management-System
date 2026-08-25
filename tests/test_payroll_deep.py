import pytest
from decimal import Decimal
from django.utils import timezone
from apps.payroll.models import SalaryStructure, PayrollRun, Payslip, TaxDeclaration, EmployeeSalaryAssignment
from apps.payroll.services import PayrollCalculationService
from apps.payroll.engine import IndianIncomeTaxEngine
from apps.employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestPayrollDeepSuite:
    def setup_method(self):
        self.user = User.objects.create_user(username="payroll.deep.user", password="Password@123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id="EMP-PAY-DEEP-01",
            first_name="Deepak",
            last_name="Sharma",
            email="deepak.pay@example.com",
            date_of_joining=timezone.now().date(),
            employment_status='ACTIVE'
        )
        self.struct = SalaryStructure.objects.create(
            name="Principal Architect Band",
            code="BAND-PRIN-01",
            annual_ctc=Decimal('2400000.00'),
            basic_percentage=Decimal('40.00'),
            hra_percentage=Decimal('20.00'),
            da_percentage=Decimal('10.00'),
            special_allowance=Decimal('20000.00'),
            conveyance_allowance=Decimal('2000.00'),
            medical_allowance=Decimal('1500.00'),
            pf_employee_rate=Decimal('12.00'),
            professional_tax=Decimal('200.00')
        )
        self.assign = EmployeeSalaryAssignment.objects.create(
            employee=self.emp,
            salary_structure=self.struct,
            bank_name="State Bank of India",
            bank_account_number="123456789012",
            pan_number="ABCDE9999F",
            tax_regime="NEW"
        )

    def test_monthly_ctc_and_components(self):
        assert self.struct.monthly_ctc == Decimal('200000.00')
        assert self.struct.monthly_basic == Decimal('80000.00')
        assert self.struct.monthly_hra == Decimal('16000.00')
        assert self.struct.monthly_da == Decimal('8000.00')
        assert self.struct.monthly_pf_employee == Decimal('9600.00')
        assert self.struct.monthly_gross > Decimal('100000.00')

    def test_payroll_run_calculation_pipeline(self):
        run = PayrollRun.objects.create(
            title="Deep Test Cycle - August 2026",
            payroll_month=8,
            payroll_year=2026,
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        updated_run = PayrollCalculationService.execute_payroll_run(run)
        assert updated_run.status == 'APPROVED'
        payslip = Payslip.objects.get(payroll_run=updated_run, employee=self.emp)
        assert payslip.gross_earnings > Decimal('0.00')
        assert payslip.net_salary > Decimal('0.00')
        assert payslip.pf_employee == Decimal('9600.00')
        assert payslip.professional_tax == Decimal('200.00')

    def test_income_tax_regime_comparison(self):
        comp = IndianIncomeTaxEngine.generate_regime_comparison(
            gross_annual_salary=Decimal('2400000.00'),
            basic=Decimal('960000.00'),
            hra=Decimal('192000.00'),
            rent=Decimal('240000.00'),
            deductions_80c=Decimal('150000.00'),
            ded_80d=Decimal('25000.00')
        )
        assert 'recommended_regime' in comp
        assert comp['new_regime']['total_annual_tax'] > Decimal('0.00')
        assert comp['old_regime']['total_annual_tax'] > Decimal('0.00')

    def test_tax_declaration_creation(self):
        dec = TaxDeclaration.objects.create(
            employee=self.emp,
            financial_year="2026-2027",
            regime="NEW",
            section_80c_lic=Decimal('50000.00'),
            section_80c_ppf=Decimal('50000.00'),
            section_80d_self=Decimal('20000.00'),
            status="SUBMITTED"
        )
        assert dec.status == "SUBMITTED"
        assert dec.section_80c_lic == Decimal('50000.00')
