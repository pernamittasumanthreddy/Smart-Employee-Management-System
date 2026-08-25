from django import forms

from apps.performance.models import PerformanceEvaluation, ReviewCycle


class PerformanceEvaluationForm(forms.ModelForm):
    class Meta:
        model = PerformanceEvaluation
        fields = [
            'employee', 'cycle', 'technical_skills_rating', 'communication_rating',
            'productivity_rating', 'leadership_rating', 'strengths', 'areas_of_improvement', 'manager_comments'
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'cycle': forms.Select(attrs={'class': 'form-select'}),
            'technical_skills_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1.0', 'max': '5.0'}),
            'communication_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1.0', 'max': '5.0'}),
            'productivity_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1.0', 'max': '5.0'}),
            'leadership_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1.0', 'max': '5.0'}),
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'areas_of_improvement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manager_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReviewCycleForm(forms.ModelForm):
    class Meta:
        model = ReviewCycle
        fields = ['title', 'code', 'start_date', 'end_date', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
