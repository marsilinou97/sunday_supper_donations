from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='input_index'),
    path('get_donor_list/', views.get_donor_list, name='get_donor_list')
]