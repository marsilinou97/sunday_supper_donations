from django.shortcuts import render
from .forms import RawDataForm
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



            # Handles case where donation category filter set to All
            if donation_type == 'all':
                filter_type = donation_type
                funds = SelectAllFunds()
                clothing = SelectAllClothings()
                giftcards = SelectAllGiftCards()
                miscellaneous = SelectAllMiscellaneous()

                # Need to filter all donations based on form filter fields before returning context

                context = {
                    "form": form,
                    "funds": funds,
                    "clothing": clothing,
                    "giftcards": giftcards,
                    "miscellaneous": miscellaneous,
                    'filter_type': filter_type
                }
            # Handles case where filter set to Funds
            elif donation_type == "fund":
                filter_type = donation_type
                funds = SelectAllFunds()

                # Need to filter funds based on form filter fields before returning context

                context = {
                    "form": form,
                    "funds": funds,
                    'filter_type': filter_type
                }

            # Handles case where donation category filter set to Giftcards
            elif donation_type == 'giftcard':
                filter_type = donation_type
                giftcards = SelectAllGiftCards()

                # Need to filter giftcards based on form filter fields before returning context

                context = {
                    "form": form,
                    "giftcards": giftcards,
                    'filter_type': filter_type
                }

            # Handles case where donation category filter set to clothing
            elif donation_type == 'clothing':
                filter_type = donation_type
                clothing = SelectAllClothings()

                # Need to filter clothing based on form filter fields before returning context

                context = {
                    "form": form,
                    "clothing": clothing,
                    'filter_type': filter_type
                }

            # Handles case where donation category filter set to miscellaneous
            elif donation_type == 'misc':
                filter_type = donation_type
                miscellaneous = SelectAllMiscellaneous()

                # Need to filter miscellaneous based on form filter fields before returning context

                context = {
                    "form": form,
                    "miscellaneous": miscellaneous,
                    'filter_type': filter_type
                }
            else:
                '''
                   Need to Handle case for Food
                '''




            return render(request, 'analytics/rawdata.html', context)

        else:
            # Form not valid
            return render(request, 'analytics/rawdata.html', {'form': form})

