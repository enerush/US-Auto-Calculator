from django import forms
from datetime import date
from numpy import arange
from calculator.models import *


class InputForm(forms.Form):
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
        super(InputForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_input'

    price = forms.IntegerField(label='Вартість авто', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'placeholder': ' 8350.00'}))
    year = forms.TypedChoiceField(label='Рік виготовлення', label_suffix='', choices=CHOICES_YEARS)
    engine_type = forms.TypedChoiceField(label='Тип двигуна', label_suffix='', choices=CHOICES_ENGINE_TYPE)
    engine_cc = forms.TypedChoiceField(label="Об'єм двигуна", label_suffix='', choices=CHOICES_ENGINE_CC)
    kwh = forms.IntegerField(label="Батарея (кВ.ч)", label_suffix='', required=False,
                               widget=forms.NumberInput(attrs={'placeholder': 'тільки для електроавтомобілей'}))
    auction_name = forms.TypedChoiceField(label='Аукціон', label_suffix='', choices=CHOICES_AUCTION)
    city = forms.TypedChoiceField(label='Площадка', label_suffix='', choices=CHOICES_CITY)
    repair_cost = forms.IntegerField(label='Ремонтні роботи', label_suffix='', min_value=0,
                                     widget=forms.NumberInput(attrs={'placeholder': ' 2500.00'}))
    company_fee = forms.IntegerField(label='Послуги фірми', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'placeholder': ' 1000.00'}))


class ResultForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_input'

    price = forms.IntegerField(label='Вартість авто', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    auction_fee = forms.IntegerField(label='Аукціонний збір', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    bank_fee = forms.IntegerField(label='Комісія банку', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    ship_cost = forms.IntegerField(label='Логістика', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    port_unload = forms.IntegerField(label='Розвантаження', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    broker = forms.IntegerField(label='Таможений брокер', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    import_fee = forms.IntegerField(label='Розмитнення', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    company_fee = forms.IntegerField(label='Послуги фірми', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    repair_cost = forms.IntegerField(label='Ремонтні роботи', label_suffix='', min_value=0,
                                     widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    tow_cost = forms.IntegerField(label='Евакуатор', label_suffix='', min_value=0,
                                     widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    certificate_euro5 = forms.IntegerField(label='Сертифікат ЄВРО5', label_suffix='', min_value=0,
                                     widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    car_registration = forms.IntegerField(label='Послуги ТСЦ', label_suffix='', min_value=0,
                                           widget=forms.NumberInput(
                                               attrs={'readonly': 'readonly', 'placeholder': '0.00'}))
    total = forms.IntegerField(label='Разом', label_suffix='', min_value=0,
                               widget=forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': '0.00'}))


