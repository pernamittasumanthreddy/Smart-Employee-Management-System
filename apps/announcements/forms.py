from django import forms

from apps.announcements.models import Announcement, CompanyEvent


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'category', 'target_department', 'publish_date', 'expiry_date', 'is_pinned', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'target_department': forms.Select(attrs={'class': 'form-select'}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class CompanyEventForm(forms.ModelForm):
    class Meta:
        model = CompanyEvent
        fields = ['title', 'event_date', 'location', 'registration_required', 'max_participants', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
