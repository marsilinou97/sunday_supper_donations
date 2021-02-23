"""sunday_supper_donations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from input import views as input_views
from news import views as news_views
from users import views as users_views

urlpatterns = [
    path('', users_views.register, name="register"),
    path('input/', input_views.index, name="input_page"),
    path('admin/', admin.site.urls, name="admin"),
    path('register/', users_views.register, name="register"),
    path('news/', news_views.index, name="news"),
]
