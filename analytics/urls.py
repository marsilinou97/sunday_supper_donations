from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='analytics_index'),
    path('rawdata/', views.raw_data, name='rawdata')
]
