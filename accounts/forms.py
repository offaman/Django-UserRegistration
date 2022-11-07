from django.forms import ModelForm
from accounts.models import Account
from django import forms


class registerationForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password']
        labels = {
            'username': ('username'),
        }
        widgets = {
            'password': forms.PasswordInput(),
        } 
        

class loginForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']


class deleteForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email']


class deleteConfirmation(ModelForm):
    class Meta:
        model = Account
        fields = fields = ['password']


class forgetForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email']


class changepasswordForm(ModelForm):
    class Meta:
        model = Account
        fields = ['password']
        labels = {
            'username': ('New password'),
        }