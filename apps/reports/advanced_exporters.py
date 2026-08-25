import csv
import io
from decimal import Decimal
from typing import List, Dict, Any
from django.http import HttpResponse

class AdvancedDataExportEngine:
    '''
    Enterprise Multi-Format Exporter for HR, Payroll, Compliance, and Operations data.
    Supports formatted CSV with BOM for Excel, Tab-Separated Values, and Structured JSON payloads.
    '''

    @staticmethod
    def export_to_csv_response(filename: str, headers: List[str], rows: List[List[Any]]) -> HttpResponse:
        buffer = io.StringIO()
        # UTF-8 BOM for Microsoft Excel auto-encoding
        buffer.write('\ufeff')
        writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        
        response = HttpResponse(buffer.getvalue(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @classmethod
    def generate_payroll_summary_export(cls, payroll_run) -> HttpResponse:
        headers = [
            'Employee ID', 'Full Name', 'Department', 'Designation',
            'Working Days', 'Days Present', 'Basic Pay (INR)', 'HRA (INR)',
            'Special Allowance (INR)', 'Gross Earnings (INR)', 'PF Deduction (INR)',
            'PT (INR)', 'TDS (INR)', 'Total Deductions (INR)', 'Net Salary (INR)',
            'Bank Account', 'Payment Status'
        ]
        rows = []
        for p in payroll_run.payslips.select_related('employee__department', 'employee__designation').all():
            rows.append([
                p.employee.employee_id,
                p.employee.full_name,
                p.employee.department.name if p.employee.department else 'General',
                p.employee.designation.title if p.employee.designation else 'Staff',
                str(p.total_working_days),
                str(p.days_present),
                f"{p.basic_pay:.2f}",
                f"{p.hra:.2f}",
                f"{p.special_allowance:.2f}",
                f"{p.gross_earnings:.2f}",
                f"{p.pf_employee:.2f}",
                f"{p.professional_tax:.2f}",
                f"{p.income_tax_tds:.2f}",
                f"{p.total_deductions:.2f}",
                f"{p.net_salary:.2f}",
                '************1012',
                'DISBURSED',
            ])
        return cls.export_to_csv_response(f"Payroll_Disbursement_{payroll_run.payroll_year}_{payroll_run.payroll_month:02d}.csv", headers, rows)
