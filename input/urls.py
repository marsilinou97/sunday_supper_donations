from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='input_index'),
    path('get_donor_list/', views.get_donor_list, name='get_donor_list'),
    path('get_donors/', views.view_get_donors, name='get_donors'),
    path('edit_businesses/', views.edit_businesses, name='edit_businesses'),
    path('add_businesses/', views.add_businesses, name='add_businesses'),
    path('edit_businesses/delete_businesses/', views.delete_businesses, name='edit_businesses_delete_businesses'),
    path('edit_businesses/get_businesses/', views.get_businesses, name='edit_businesses_get_businesses'),
    path('edit_businesses/update_businesses/', views.update_businesses, name='edit_businesses_update_businesses')
]
