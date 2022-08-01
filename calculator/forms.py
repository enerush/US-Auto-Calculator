from django import forms
from datetime import date
from .models import *


class CreateNewCount(forms.Form):
    url = forms.URLField(label='URL', required=False)
    price = forms.IntegerField(label='Price', min_value=0)
    year = forms.IntegerField(label='Year', min_value=1950, max_value=date.today().year)
    engine_type = forms.ChoiceField(label='Type', choices=(
                                                    ('GAS', "Бензин"), ('DIESEL', "Дизель"), ('ELECTRIC', 'Електро')))
    engine_cc = forms.FloatField(label="Engine", min_value=0.5, max_value=7.5)
    auction_name = forms.CharField(label='Auction', max_length=6)
    city = forms.CharField(label='City', max_length=50)