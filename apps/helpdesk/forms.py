from django import forms

from apps.helpdesk.models import SupportTicket, TicketMessage


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['category', 'subject', 'priority', 'description', 'attachment']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description of the issue'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed steps to reproduce or details of the request...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a response...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TicketResolveForm(forms.Form):
    resolution_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Document final resolution provided...'})
    )
