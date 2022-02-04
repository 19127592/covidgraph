
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='homepage'),

    path('test-page', views.test,name='test'),
    path('test-page/count-words',views.count,name='count'),

    path('user-manual',views.user_manual,name='manual'),
    path('register-person',views.register,name='register'),
    path('search',views.search,name='search'),

    path('login-account',views.login,name='login'),
    path('signup-account',views.signup,name='signup'),
    
    path('about-us',views.about,name='about')
]
