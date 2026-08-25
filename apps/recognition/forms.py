from django import forms

from apps.recognition.models import EmployeeRecognition


class RecognitionForm(forms.ModelForm):
    class Meta:
        model = EmployeeRecognition
        fields = ['recipient', 'category', 'title', 'message']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Outstanding assistance during system migration'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explain how this colleague made a difference...'}),
        }
