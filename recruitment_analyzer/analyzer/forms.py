# analyzer/forms.py

from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'name',
            'email',
            'phone_number',
            'job_position',
            'resume',
            'cover_letter'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'job_position': forms.TextInput(attrs={'placeholder': 'Position you are applying for'}),
            'resume': forms.ClearableFileInput(attrs={'placeholder': 'Upload your resume'}),
            'cover_letter': forms.ClearableFileInput(attrs={'placeholder': 'Optional: Upload a cover letter'}),
        }

class JobApplicationStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
