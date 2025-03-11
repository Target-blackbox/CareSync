from django import forms
from .models import Patient

class PatientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    phone = forms.CharField(
        max_length=10, 
        min_length=10, 
        widget=forms.TextInput(attrs={"pattern": "[0-9]{10}"}), 
        error_messages={"min_length": "Phone number must be exactly 10 digits.", 
                        "max_length": "Phone number must be exactly 10 digits."}
    )

    class Meta:
        model = Patient
        fields = ["name", "email", "phone", "password"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data


class PatientLoginForm(forms.Form):
    name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your name"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )