from django import forms
from django.db import models
from django.forms import fields,ModelChoiceField
from .models import Car, CarModel


class CarForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea())
    title=forms.CharField(widget=forms.TextInput())
    carmodel=forms.ModelChoiceField(queryset=CarModel.objects.all())
    class Meta:
        model=Car
        fields=['title','car_type','description','carmodel','image','video','cities','year','capacity_engine','fuel','engine_power','kilometers','body_type','color','technical_condiation','transmissions','wheel','price']