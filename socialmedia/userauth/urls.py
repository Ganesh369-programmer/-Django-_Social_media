
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from userauth import views 

urlpatterns = [
 
    path('', views.home),
    path('signup/' , views.signup , name='signup'),
    path('login/' ,  views.loginn , name='loginn'),
    path('logout/' , views.logoutt , name ='logoutt'),
    path('upload/' , views.upload , name='upload') , 
]
