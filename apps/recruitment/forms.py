from django import forms
from apps.recruitment.models import JobRequisition, Candidate, JobApplication, InterviewSchedule, OfferLetter

class JobRequisitionForm(forms.ModelForm):
    class Meta:
        model = JobRequisition
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'requisition_code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'headcount': forms.NumberInput(attrs={'class': 'form-control'}),
            'hiring_manager': forms.Select(attrs={'class': 'form-select'}),
            'min_experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'work_location': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control'}),
            'target_hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'current_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'total_experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_ctc': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_ctc': forms.NumberInput(attrs={'class': 'form-control'}),
            'notice_period_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'skills_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
