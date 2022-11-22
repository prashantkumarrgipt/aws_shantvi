from nturl2path import url2pathname
from django.contrib import admin
from django.urls import path,include
from blog1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('category/<str:url>', views.category,name='blogcategory'),
    path('tags/<str:name>', views.tags,name='tags'),
    path('contact', views.blogcontact,name='blogcontact'),
    path('about', views.blogabout,name='blogabout'),
    path('<str:slug>', views.post,name='post'),
    
    path('category/', views.common,name='common'),
    path('section/', views.section,name='section'),
    path('', views.common,name='common'),
    

]
