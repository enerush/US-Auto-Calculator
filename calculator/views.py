from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import *
from .services.services import *

menu = ['Головна сторінка', 'Калькулятор']


def index(request):
    if request.method == 'POST':
        form = CreateNewCount(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = CreateNewCount()
    return render(request, 'calculator/index.html', {'form': form, 'title': menu[1]})


def calculate(request):
    form = CreateNewCount(request.POST)
    res = get_total_cost(request)
    return render(request, 'calculator/result.html', {'form': form, 'result': res})

