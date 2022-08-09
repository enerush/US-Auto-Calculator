from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('carfax/', carfax, name='carfax'),
    path('decoder/', decoder, name='decoder'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('login/', login, name='login')
]
