from urllib import request
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request,'mainpage/home.html')

def user_manual(request):
    return render(request,'manual/manual.html')

def register(request):
    return render(request,'register/manual.html')

def search(request):
    return render(request,'search/search.html')

def test(request):
    return HttpResponse('Test page')
