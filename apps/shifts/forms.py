from django import forms

from apps.shifts.models import CompanyHoliday, ShiftAssignment, WorkShift


class WorkShiftForm(forms.ModelForm):
    class Meta:
        model = WorkShift
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'grace_period_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'half_day_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'full_day_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_night_shift': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ShiftAssignmentForm(forms.ModelForm):
    class Meta:
        model = ShiftAssignment
        fields = ['employee', 'shift', 'start_date', 'end_date', 'is_active']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CompanyHolidayForm(forms.ModelForm):
    class Meta:
        model = CompanyHoliday
        fields = ['name', 'date', 'description', 'is_optional', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_optional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }
