from django.http import HttpResponse
from django.shortcuts import render

def movies(request):
    return render(request, 'movies/movies.html')

def home(request):
    return HttpResponse("Welcome to the home page")

