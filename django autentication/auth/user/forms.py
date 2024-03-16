from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

class LoginForm(forms.Form):
    email=forms.EmailField(label="Enter Email",max_length=100,validators=[MinLengthValidator(20)])
    password=forms.CharField(widget=forms.PasswordInput,validators=[MinLengthValidator(20)])

  