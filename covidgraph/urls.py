
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('test-page', views.test),
    path('user-manual',views.user_manual),
    path('register',views.register),
    path('search',views.search),
]
