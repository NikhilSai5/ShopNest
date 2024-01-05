# forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'class': 'Rusername'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'Rusername'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'Rusername'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'Rusername'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


# forms.py


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'class': 'Lusername'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'Lpassword'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and not password:
            raise forms.ValidationError("Please enter your password.")

        return cleaned_data
