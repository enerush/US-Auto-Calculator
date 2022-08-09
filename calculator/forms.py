from django import forms
from datetime import date
from numpy import arange
from calculator.models import *


class CalculatorForm(forms.Form):
    CHOICES_YEARS = ((year, year) for year in range(date.today().year, 1950, -1))

    CHOICES_ENGINE_TYPE = (('GAS', "Бензин"),
                           ('DIESEL', "Дизель"),
                           ('ELECTRIC', 'Електро'),
                           ('HYBRID', 'Гібрид'))
    CHOICES_ENGINE_CC = ((round(cc, 1), round(cc, 1)) for cc in arange(0, 10, 0.1))
    CHOICES_AUCTION = (('Copart', 'Copart'),
                       ('IAAI', 'IAAI'))

    CHOICES_CITY = [(c.city, c.city) for c in City.objects.all()]
    CHOICES_CITY = sorted(set(CHOICES_CITY))

    def __init__(self, *args, **kwargs):
        super(CalculatorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_input'

    price = forms.IntegerField(label='Ціна авто', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'placeholder': '8350.00'}))
    year = forms.TypedChoiceField(label='Рік випуску', label_suffix='', choices=CHOICES_YEARS)
    engine_type = forms.TypedChoiceField(label='Тип двигуна', label_suffix='', choices=CHOICES_ENGINE_TYPE)
    engine_cc = forms.TypedChoiceField(label="Об'єм двгуна", label_suffix='', choices=CHOICES_ENGINE_CC)
    kwh = forms.IntegerField(label="Батарея (кВ.ч)", label_suffix='', required=False,
                               widget=forms.NumberInput(attrs={'placeholder': 'тільки для електроавтомобілей'}))
    auction_name = forms.TypedChoiceField(label='Аукціон', label_suffix='', choices=CHOICES_AUCTION)
    city = forms.TypedChoiceField(label='Площадка', label_suffix='', choices=CHOICES_CITY)
    company_fee = forms.IntegerField(label='Послуги', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'placeholder': '1000.00'}))


class ResultForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_input'

    price = forms.IntegerField(label='Ціна авто', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    auction_fee = forms.IntegerField(label='Збір Аукціону', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    bank_fee = forms.IntegerField(label='Комісія банку', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    ship_cost = forms.IntegerField(label='Доставка', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    port_unload = forms.IntegerField(label='Розвантаження', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    broker = forms.IntegerField(label='Брокер', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    import_fee = forms.IntegerField(label='Розмитнення', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    company_fee = forms.IntegerField(label='Послуги', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    total = forms.IntegerField(label='Разом', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))

