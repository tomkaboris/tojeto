from django import forms
from django.contrib.auth.models import Group
from .models import UserRegistration

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Potvrdi šifru", max_length=255)

    class Meta:
        model = UserRegistration
        fields = ['email', 'full_name', 'password', 'phone_number', 'user_type_id', 'consent']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Šifre se ne poklapaju.")