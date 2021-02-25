from django.shortcuts import render
from .forms import RawDataForm
import logging

from .queries import *


def index(request):
    return render(request, 'analytics/analytics.html')


def raw_data(request):

    form = RawDataForm()

    # Handles GET request
    if request.method == 'GET':
        return render(request, 'analytics/rawdata.html', {'form': form})
    else:
        # Handles POST request
        form = RawDataForm(request.POST)

        if form.is_valid():


            # retrieve valid filter fields from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            donation_date = form.cleaned_data['donation_date']
            donation_type = form.cleaned_data['donation_type']

            #temp print for debugging
            print(first_name + " : " + last_name + " : " + str(donation_date) + " : " + donation_type)

            '''
            1.) Run queries based on retrieved filter fields
            2.) return form context with filtered data
            
            '''


            return render(request, 'analytics/rawdata.html', {'form': form})

        else:
            # Form not valid
            return render(request, 'analytics/rawdata.html', {'form': form})

