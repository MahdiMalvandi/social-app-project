from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
