from django.shortcuts import render
from django.http import request

# Create your views here.
def home(request):
    return render(request, 'Inno_Consulting/home.html')