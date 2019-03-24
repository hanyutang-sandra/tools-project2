"""tools2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf.urls import url, include
from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
import sunscreen.views

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^$', sunscreen.views.front, name='front'),

    re_path(r'^register$', sunscreen.views.register, name='register'),
    re_path(r'^login$', sunscreen.views.login, name='login'),
    re_path(r'^join$', sunscreen.views.join, name='join'),

]
