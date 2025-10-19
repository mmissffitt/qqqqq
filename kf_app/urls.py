from django.urls import path
from .views import root
from django.shortcuts import render

# Добавьте временные view-функции для всех страниц
def movies_view(request):
    return render(request, 'movies.html')

def series_view(request):
    return render(request, 'series.html')

def subscriptions_view(request):
    return render(request, 'subscriptions.html')

urlpatterns = [
    path('', root, name='index'),
    path('movies/', movies_view, name='movies'),
    path('series/', series_view, name='series'),
    path('subscriptions/', subscriptions_view, name='subscriptions'),
]