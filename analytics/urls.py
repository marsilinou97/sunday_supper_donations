from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='analytics_index'),
    path('rawdata/', views.raw_data, name='analytics_rawdata'),
    path('rawdata/download_my_file/', views.download, name='download_my_file'),
    path('edit_donations/', views.edit_donations, name='analytics_edit_donations'),
    path('edit_donations/get_table/', views.get_table, name='edit_donations_get_table'),
    path('edit_donors/', views.edit_donors, name='analytics_edit_donors'),
    path('edit_donors/get_table/', views.edit_donors_get_table, name='edit_donors_get_table'),
    path('edit_donors/update_donor/', views.update_donor, name='edit_donors_update_donor'),
    path('get_donation_count_date_qty/', views.get_donation_count_date_qty, name='get_donation_count_date_qty'),
    path('get_donation_count_month/', views.get_donation_count_month, name='get_donation_count_month'),
    path('get_donation_item_count/', views.get_donation_item_count, name='get_donation_item_count'),
    path('get_donation_fund_count/', views.get_donation_fund_count, name='get_donation_fund_count'),
    path('edit_donations/update_item/', views.update_item, name='update_item'),
    path('edit_donations/delete_item/', views.delete_item, name='delete_item'),
    path('rawdata/get_table/', views.get_table, name='rawdata_get_table'),

]
