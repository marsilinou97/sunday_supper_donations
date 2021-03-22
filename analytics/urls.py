from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='analytics_index'),
    path('rawdata/', views.raw_data, name='analytics_rawdata'),
    path('piechart/', views.pie_chart, name='analytics_piechart'),
    path('linechart/', views.line_chart, name='analytics_linechart'),
    path('edit_donations/', views.edit_donations, name='analytics_edit_donations'),
    path('edit_donations/get_table/', views.get_table, name='edit_donations_get_table'),
    path('edit_donations/delete_fund/', views.delete_fund, name='edit_donations_delete_fund'),
]
