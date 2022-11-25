"""study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from turtle import home1
from django.contrib import admin
from django.urls import path ,include
from django.views.static import serve 
from django.conf import settings
from django.conf.urls.static import static
# from django.urls import re_path as url
# from django.conf.urls import url
from django.urls import include, re_path as url

admin.site.site_header = "Shantvi Admin"
admin.site.site_title = "Shantvi Admin Panel"
admin.site.index_title = "Welcome to Shantvi Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home1.urls')),
    path('blog/', include('blog1.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
]
# ]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
