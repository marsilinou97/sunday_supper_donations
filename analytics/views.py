from django.shortcuts import render
from .forms import RawDataForm

def index(request):
    return render(request, 'analytics/analytics.html')

def raw_data(request):

    form = RawDataForm()

    if request.method == 'GET':
        return render(request, 'analytics/rawdata.html', {'form': form})
    else:
        # Handles POST request
        form = RawDataForm(request.POST)

        '''
        Process form to run queries on DB....
        '''


