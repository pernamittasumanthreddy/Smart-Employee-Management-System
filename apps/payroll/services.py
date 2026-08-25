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
        employees = Employee.objects.filter(employment_status='ACTIVE')
        if not employees.exists():
            employees = Employee.objects.all()
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
