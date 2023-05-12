from django import forms

class LoginForm(forms.Form):
    log_login = forms.CharField(max_length=30)
    log_password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    reg_login = forms.CharField(max_length=30)
    reg_email = forms.CharField(max_length=100)
    reg_password = forms.CharField(widget=forms.PasswordInput)