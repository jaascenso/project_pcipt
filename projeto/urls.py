"""projeto URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from historia.views import *

from django.contrib import admin

admin.site.site_header = 'Petições Coloniais no Império Português'              
admin.site.index_title = 'Utilizadores e administração da base de dados'        
admin.site.site_title = 'Utilizadores e administração da base de dados'         

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls, name='myadmin'),
    path('migracao/', migracao, name='migracao'),
    path('loading/', loading, name='loading')
]
