from turtle import width
from urllib import request
from django.shortcuts import render

import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

def home(request):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green'))

    fig.update_layout(width=500,height=300)
    
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request,'mainpage/homepage/home.html', context={'plot_div': plot_div})

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
