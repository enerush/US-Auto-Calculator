from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import *
from .services.services import *

menu = [{'title': 'Carfax', 'url_name': 'carfax'},
        {'title': 'VIN Decoder', 'url_name': 'decoder'},
        {'title': 'Контакти', 'url_name': 'contact'},
        {'title': 'Про нас', 'url_name': 'about'},
        {'title': 'Вхід', 'url_name': 'login'}]


def index(request):
    context = {'input_form': InputForm(),
               'res_form': ResultForm(),
               'menu': menu,
               'title': 'US Auto Calculator: Калькулятор розрахунку'}

    if request.method == 'POST':
        if 'url' in request.POST and 'price' not in request.POST:
            request.POST = request.POST.copy()
            scan = ScanData(request)
            request = scan.get_data()
            context['input_form'] = InputForm(request.POST)
            return render(request, 'calculator/index.html', context=context)

        calc = Calculator(request)
        context['input_form'] = InputForm(request.POST)
        context['res_form'] = ResultForm(calc())
        return render(request, 'calculator/index.html', context=context)
    return render(request, 'calculator/index.html', context=context)


def carfax(request):
    context = {
        'menu': menu,
        'title': 'US Auto Calculator: Carfax звіт'
    }
    return render(request, 'calculator/carfax.html', context=context)


def decoder(request):
    context = {
        'menu': menu,
        'title': 'US Auto Calculator: VIN decoder'
    }
    return render(request, 'calculator/decoder.html', context=context)


def contact(request):
    context = {
        'menu': menu,
        'title': 'US Auto Calculator: Контакти'
    }
    return render(request, 'calculator/contact.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'US Auto Calculator: Про нас'
    }
    return render(request, 'calculator/about.html', context=context)


def login(request):
    context = {
        'menu': menu,
        'title': 'US Auto Calculator: Вхід'
    }
    return render(request, 'calculator/login.html', context=context)

