from django.shortcuts import render
from .forms import RawDataForm
from .queries import *


def index(request):
    return render(request, 'analytics/analytics.html')


def raw_data(request):
    form = RawDataForm()

    funds = SelectAllFunds()
    clothing = SelectAllClothings()
    giftcards = SelectAllGiftCards()
    miscellaneous = SelectAllMiscellaneous()

    # Handles GET request
    if request.method == 'GET':

        context = {
            "form": form,
            "funds": funds,
            "clothing": clothing,
            "giftcards": giftcards,
            "miscellaneous": miscellaneous
        }

    else:
        # Handles POST request

        form = RawDataForm(request.POST)

        if form.is_valid():
            # retrieve valid filter fields from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            donation_date = form.cleaned_data['donation_date']

            #TODO: Filter tables based on form fields before returning context

            context = {
                "form": form,
                "funds": funds,
                "clothing": clothing,
                "giftcards": giftcards,
                "miscellaneous": miscellaneous
            }

    # Return populated context based on HTTP request
    return render(request, 'analytics/rawdata.html', context)
