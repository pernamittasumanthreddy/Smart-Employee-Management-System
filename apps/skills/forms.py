from django import forms

from apps.skills.models import (
    EmployeeSkill,
    ProjectSkillRequirement,
    Skill,
)


class EmployeeSkillForm(forms.ModelForm):
    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'proficiency_level', 'years_of_experience']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'proficiency_level': forms.Select(attrs={'class': 'form-select'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name', 'code', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ProjectSkillRequirementForm(forms.ModelForm):
    class Meta:
        model = ProjectSkillRequirement
        fields = ['skill', 'min_proficiency']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'min_proficiency': forms.Select(attrs={'class': 'form-select'}),
        }
