import django
from django.db.models.fields import IntegerField
from django.forms import widgets
import django_filters
from django_filters import CharFilter
from django_filters.filters import ChoiceFilter,BaseInFilter, DateFilter, DateFromToRangeFilter, DateRangeFilter, DateTimeFromToRangeFilter
from .models import Car,Color,Cities,CarModel, voivodeship,Condation,body,wheel
from django import forms


class CarFilter(django_filters.FilterSet):
    color = django_filters.ModelChoiceFilter(empty_label="Colors",label='Choose Colors', queryset=Color.objects.all())
    cities = django_filters.ModelChoiceFilter(empty_label="Choose Cities", queryset=Cities.objects.all())
    carmodel = django_filters.ModelChoiceFilter(empty_label="Choose Model", queryset=CarModel.objects.all())
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    body= django_filters.ModelChoiceFilter(empty_label="Body",label='Choose Body', queryset=body.objects.all())
    wheel=django_filters.ModelChoiceFilter(empty_label="Wheel",label='Choose Wheel', queryset=wheel.objects.all())
    year=django_filters.RangeFilter(label='From To Year')
    technical_condiation= django_filters.ModelChoiceFilter(empty_label="Condiation",label='Choose Condiation', queryset=Condation.objects.all())
    class Meta:
        model = Car
        fields = ['color','cities','carmodel']