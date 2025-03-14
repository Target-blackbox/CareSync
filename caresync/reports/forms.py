from django import forms
from .models import ReportFolder, Report

class ReportFolderForm(forms.ModelForm):
    class Meta:
        model = ReportFolder
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter folder name'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter report title'}),
            'file': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.csv'}), # example file types
        }