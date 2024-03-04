# forms.py
from django import forms
from .models import Bus, Station

class AddRouteForm(forms.Form):
    bus = forms.ModelChoiceField(queryset=Bus.objects.all())
    start_station = forms.ModelChoiceField(queryset=Station.objects.all())
    end_station = forms.ModelChoiceField(queryset=Station.objects.all())
    stops = forms.ModelMultipleChoiceField(queryset=Station.objects.all(), widget=forms.CheckboxSelectMultiple)
