from urllib import request
from django.shortcuts import render

from collections import Counter

def home(request):
    return render(request,'mainpage/homepage/home.html')

def about(request):
    return render(request,'mainpage/about/about.html')

def user_manual(request):
    return render(request,'mainpage/manual/manual.html')

def register(request):
    return render(request,'mainpage/register/register.html')

def search(request):
    return render(request,'mainpage/search/search.html')

def login(request):
    return render(request,'mainpage/auth/login.html')

def signup(request):
    return render(request,'mainpage/auth/signup.html')

def test(request):
    return render(request,'mainpage/test/test.html')

def count(request):
    fulltext = request.GET['fulltext']
    countwords = fulltext.split()
    worddict = dict()
    for word in countwords:
        if word in worddict:
            worddict[word]+= 1
        else:
            worddict[word] = 1
    max_value = max(worddict.values())
    
    most_frequent = [(word,value) for word,value in worddict.items() if value==max_value]

    return render(request,'mainpage/test/count.html',{'fulltext':fulltext,'count':len(countwords),'most_frequent':most_frequent})
