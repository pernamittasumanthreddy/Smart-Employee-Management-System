import pytest
from decimal import Decimal
from django.utils import timezone
from apps.payroll.models import SalaryStructure, PayrollRun, Payslip, TaxDeclaration
from apps.payroll.services import PayrollCalculationService
from apps.payroll.engine import IndianIncomeTaxEngine
from apps.employees.models import Employee

@pytest.mark.django_db
def test_salary_structure_calculations():
    struct = SalaryStructure.objects.create(
        name="Tech Lead Band",
        code="TL-B1",
        annual_ctc=Decimal('1200000.00'),
        basic_percentage=Decimal('40.00'),
        hra_percentage=Decimal('20.00'),
        da_percentage=Decimal('10.00'),
        pf_employee_rate=Decimal('12.00'),
        professional_tax=Decimal('200.00')
    )
    assert struct.monthly_ctc == Decimal('100000.00')
    assert struct.monthly_basic == Decimal('40000.00')
    assert struct.monthly_hra == Decimal('8000.00')
    assert struct.monthly_da == Decimal('4000.00')
    assert struct.monthly_pf_employee == Decimal('4800.00')
    assert struct.monthly_gross > Decimal('50000.00')

@pytest.mark.django_db
def test_indian_income_tax_engine():
    # Test New Regime Standard Deduction
    res_new = IndianIncomeTaxEngine.compute_new_regime_tax(Decimal('600000.00'))
    assert res_new['total_annual_tax'] == Decimal('0.00')  # 87A rebate applies under 7L

    # Test Higher Income in New Regime
    res_high = IndianIncomeTaxEngine.compute_new_regime_tax(Decimal('1500000.00'))
    assert res_high['total_annual_tax'] > Decimal('0.00')

    # Test Old Regime
    res_old = IndianIncomeTaxEngine.compute_old_regime_tax(
        gross_annual_salary=Decimal('1200000.00'),
        annual_basic=Decimal('480000.00'),
        annual_hra_received=Decimal('96000.00'),
        annual_rent_paid=Decimal('180000.00'),
        sec_80c_total=Decimal('150000.00'),
        sec_80d_self=Decimal('25000.00')
    )
    assert res_old['hra_exemption'] > Decimal('0.00')
    assert res_old['chapter_via_deductions'] == Decimal('175000.00')

@pytest.mark.django_db
def test_payroll_run_execution(client):
    run = PayrollRun.objects.create(
        title="Test Cycle - August 2026",
        payroll_month=8,
        payroll_year=2026,
        start_date=timezone.now().date(),
        end_date=timezone.now().date()
    )
    updated_run = PayrollCalculationService.execute_payroll_run(run)
    assert updated_run.status == 'APPROVED'
    assert updated_run.payslips.count() >= 0
