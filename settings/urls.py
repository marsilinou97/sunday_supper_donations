from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='settings_index'),
    path('change_password/', views.change_password, name='change_password'),
    path('manage_roles/', views.manage_roles, name='manage_roles'),
    path('manage_registration_links', views.manage_registration_links, name='manage_registration_links'),
    path('manage_registration_links/get_table/', views.manage_registration_links_get_table, name='manage_registration_links_get_table'),
    path('help/', views.help, name='help'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
    path('get_roles/', views.get_roles, name='get_roles'),
    path('update_user_role/', views.update_user_role, name='update_user_role'),
    path('activate_user/', views.activate_user, name='activate_user')
]
