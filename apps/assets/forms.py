from django import forms

from apps.assets.models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_id', 'name', 'category', 'serial_number', 'model_number', 'purchase_date', 'purchase_cost', 'warranty_expiry_date', 'status', 'notes']
        widgets = {
            'asset_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AST-104'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'warranty_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class AssetAssignForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Assignment notes or condition...'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.employees.models import Employee
        self.fields['employee'].queryset = Employee.objects.filter(employment_status='ACTIVE')
