from django.shortcuts import render

def root(request):
    return render(request, 'index.html')

def movies_view(request):
    return render(request, 'movies.html')

def series_view(request):
    return render(request, 'series.html')

def subscriptions_view(request):
    return render(request, 'subscriptions.html')