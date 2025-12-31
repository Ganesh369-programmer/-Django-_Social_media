
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
    path('like-post<str:id>', views.likes , name = 'like-post'),
    path('#<str:id>' , views.home_posts ),
    path('explore' , views.explore ),
    path('profile/<str:id_user>' , views.profile , name='profile' ),
    path('follow' , views.follow, name='follow'),
    path('delete/<str:id>' , views.delete),
    path('search_result/' , views.search_result , name='search_results'),
    path('liked_list/' , views.like_list , name='liked_list'),
    path('comment/<uuid:post_id>/', views.add_comment, name='add-comment'),

]
