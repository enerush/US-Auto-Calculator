from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import *
from .models import *
from .services.services import *

menu = [{'title': 'Carfax', 'url_name': 'carfax'},
        {'title': 'VIN Decoder', 'url_name': 'decoder'},
        {'title': 'Контакти', 'url_name': 'contact'},
        {'title': 'Про нас', 'url_name': 'about'},
        {'title': 'Вхід', 'url_name': 'login'}]


def index(request):
    form = CalculatorForm()
    res_form = ResultForm()
    context = {'form': form,
               'res_form': res_form,
               'menu': menu,
               'title': 'Головна'}
    if request.method == 'POST':
        context['form'] = CalculatorForm(request.POST)
        context['res_form'] = get_result_form(request)
        return render(request, 'calculator/index.html', context=context)

    return render(request, 'calculator/index.html', context=context)


def carfax(request):
    return HttpResponse('Сторінка "Carfax". Сайт знаходиться в стадії розробки!')


def decoder(request):
    return HttpResponse('Сторінка "VIN Decoder". Сайт знаходиться в стадії розробки!')


def contact(request):
    return HttpResponse('Сторінка "Контакти". Сайт знаходиться в стадії розробки!')


def about(request):
    return HttpResponse('Сторінка "Про нас". Сайт знаходиться в стадії розробки!')


def login(request):
    return HttpResponse('Сторінка "Вхід". Сайт знаходиться в стадії розробки!')
