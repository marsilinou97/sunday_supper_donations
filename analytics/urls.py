from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='analytics_index'),
    path('rawdata/', views.raw_data, name='analytics_rawdata'),
    path('piechart/', views.pie_chart, name='analytics_piechart'),
    path('linechart/', views.line_chart, name='analytics_linechart'),

]
