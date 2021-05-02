from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='settings_index'),
    path('change_password/', views.change_password, name='change_password'),

    path('manage_roles/', views.manage_roles, name='manage_roles'),
    path('manage_roles/activate_user/', views.activate_user, name='activate_user'),
    path('manage_roles/get_roles/', views.get_roles, name='get_roles'),
    path('manage_roles/get_user_data/', views.get_user_data, name='manage_roles_get_user_data'),
    path('manage_roles/update_user_role/', views.update_user_role, name='update_user_role'),

    path('manage_registration_links/', views.manage_registration_links, name='manage_registration_links'),
    path('manage_registration_links/delete_token/', views.delete_token, name='delete_token'),
    path('manage_registration_links/get_token_data/', views.get_token_data, name='manage_registration_links_get_token_data'),
    path('manage_registration_links/update_token_data/', views.update_token_data, name='update_token_data'),

    path('help/', views.help, name='help'),
]
