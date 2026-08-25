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
