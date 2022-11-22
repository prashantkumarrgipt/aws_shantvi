from nturl2path import url2pathname
from django.contrib import admin
from django.urls import path,include
from home1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name='home'),
    path('contact', views.contact,name='contact'),
    path('about', views.about,name='about'),
    # path('category/', views.blogcategoryhome,name='blogcategoryhome'),
    path('blog/', include('blog1.urls')),
    path('search', views.search, name="search"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    # path('write-and-earn', views.write_and_earn, name="write_and_earn"),

]