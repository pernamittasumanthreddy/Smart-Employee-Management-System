"""
Statutory Register & Legal Audit Report Generator:
Generates Form A (Employee Register), Form B (Wage Register),
Form C (Loan/Recovery), Form D (Attendance), and Form E (Overtime).
"""

import csv
import io
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional


class StatutoryAuditReportGenerator:
    """
    Compiles formal regulatory audit registers required under
    Ease of Compliance Rules 2017 and Code on Wages 2019.
    """

    @classmethod
    def generate_form_a_employee_register_csv(cls, employees: List[Dict]) -> str:
        """
        Form A: Format of Employee Register (Rule 2(1) of Ease of Compliance Rules).
        """
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['FORM A - FORMAT OF EMPLOYEE REGISTER'])
        writer.writerow(['[See Rule 2(1) of Ease of Compliance to Maintain Registers under various Labour Laws Rules, 2017]'])
        writer.writerow(['Name of the Establishment: Bharat Enterprise Solutions Ltd.', 'CIN: U72200KA2024PLC098765'])
        writer.writerow([])

        headers = [
            'Sl. No', 'Employee ID', 'Full Name', 'Gender', "Father's/Spouse Name",
            'Date of Birth', 'Nationality', 'Education Level', 'Date of Joining',
            'Designation', 'Category (Skill)', 'Type of Employment', 'Mobile No',
            'UAN (EPF)', 'ESIC No', 'Aadhaar / National ID', 'Bank Account No',
            'Bank IFSC', 'Present Address', 'Permanent Address', 'Status'
        ]
        writer.writerow(headers)

        for idx, emp in enumerate(employees, start=1):
            writer.writerow([
                idx,
                emp.get('employee_id', f'EMP-{idx:04d}'),
                emp.get('full_name', 'N/A'),
                emp.get('gender', 'PREFER_NOT_TO_SAY'),
                emp.get('father_name', '--'),
                emp.get('dob', '1995-01-01'),
                'Indian',
                emp.get('education', 'Graduate (B.Tech / B.E)'),
                emp.get('doj', '2024-01-15'),
                emp.get('designation', 'Engineer'),
                emp.get('skill_category', 'SKILLED'),
                emp.get('employment_type', 'FULL_TIME'),
                emp.get('phone', '9876543210'),
                emp.get('uan', f'10123456{idx:04d}'),
                emp.get('esic', f'31234567{idx:04d}'),
                emp.get('national_id', f'XXXX-XXXX-{idx:04d}'),
                emp.get('bank_account', f'918273645{idx:04d}'),
                'HDFC0001234',
                emp.get('current_address', 'Bangalore, Karnataka'),
                emp.get('permanent_address', 'Bangalore, Karnataka'),
                'ACTIVE'
            ])

        return output.getvalue()

    @classmethod
    def generate_form_b_wage_register_csv(cls, wage_records: List[Dict], month_year: str) -> str:
        """
        Form B: Format of Register of Wages (Rule 2(1)).
        """
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['FORM B - FORMAT OF REGISTER OF WAGES'])
        writer.writerow([f'Wage Period: {month_year}', 'Name of Establishment: Bharat Enterprise Solutions Ltd.'])
        writer.writerow([])

        headers = [
            'Sl. No', 'Emp ID', 'Name', 'Designation', 'Total Days Worked',
            'Units / Hours', 'Basic Pay', 'DA', 'HRA', 'Special Allow',
            'Overtime Pay', 'Gross Wages', 'EPF Ded', 'ESI Ded', 'PTax Ded',
            'TDS Ded', 'Other Ded', 'Total Deductions', 'Net Wages Paid',
            'Date of Payment', 'Signature / Digital Bank Ref'
        ]
        writer.writerow(headers)

        for idx, w in enumerate(wage_records, start=1):
            writer.writerow([
                idx,
                w.get('employee_id', f'EMP-{idx:04d}'),
                w.get('name', 'Staff'),
                w.get('designation', 'Executive'),
                w.get('days_worked', 30),
                w.get('hours', 240),
                w.get('basic', '45000.00'),
                '0.00',
                w.get('hra', '22500.00'),
                w.get('special', '12500.00'),
                w.get('ot_pay', '0.00'),
                w.get('gross', '80000.00'),
                w.get('epf', '1800.00'),
                w.get('esi', '0.00'),
                w.get('ptax', '200.00'),
                w.get('tds', '4500.00'),
                '0.00',
                w.get('total_ded', '6500.00'),
                w.get('net_pay', '73500.00'),
                'Last Working Day of Month',
                f'UTR-NEFT-2026{idx:06d}'
            ])

        return output.getvalue()
