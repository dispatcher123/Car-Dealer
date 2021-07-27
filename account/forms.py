from django import forms
from django.forms import fields
from django.forms.fields import CharField
from django.forms.widgets import PasswordInput
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
        'class' : 'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password'
    }))

    class Meta:
        model=CustomUser
        fields=('email','first_name','last_name')

    def clean(self,*args, **kwargs):
        cleaned_data=super(RegistrationForm,self).clean(*args, **kwargs)
        password=self.cleaned_data['password']
        confirm_password=self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('Password Does Not Match!')


    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'