from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='settings_index'),
    path('change_password/', views.change_password, name='change_password'),
    path('manage_roles/', views.manage_roles, name='manage_roles'),
    path('manage_registration_links', views.manage_registration_links, name='manage_registration_links'),
    path('help/', views.help, name='help')
]
