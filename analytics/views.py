from django.shortcuts import render
from .forms import RawDataForm
from .queries import *
from input.models import *


def index(request):
    return render(request, 'analytics/analytics.html')


def raw_data(request):
    form = RawDataForm()

    funds = SelectAllFunds()
    food = SelectAllFood()
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

            # Filter tables based on form fields before returning context
            # Set the filters
            filters = {}
            if first_name != "" and first_name is not None:
                filters["first_name"] = first_name
            if last_name != "" and last_name is not None:
                filters["last_name"] = last_name
            if donation_date is not None:
                filters["donation_date"] = donation_date

            # If any of the filters were used, filter the results
            if len(filters) > 0:
                f_funds = FilterResults(funds,filters)
                f_clothing = FilterResults(clothing,filters)
                f_giftcards = FilterResults(giftcards,filters)
                f_food = FilterResults(food,filters)
                f_miscellaneous = FilterResults(miscellaneous,filters)

                # Reset the filters for next time
                filters = {}
                del temp_caching["SelectAllFunds"]
                del temp_caching["SelectAllClothings"]
                del temp_caching["SelectAllGiftCards"]
                del temp_caching["SelectAllFood"]
                del temp_caching["SelectAllMiscellaneous"]

                # Set the context
                context = {
                    "form": form,
                    "funds": f_funds,
                    "clothing": f_clothing,
                    "giftcards": f_giftcards,
                    "food": f_food,
                    "miscellaneous": f_miscellaneous
                }

            # If none of the filters were used, the don't filter anything
            else:
                context = {
                    "form": form,
                    "funds": funds,
                    "clothing": clothing,
                    "giftcards": giftcards,
                    "food": food,
                    "miscellaneous": miscellaneous
                }

    # Return populated context based on HTTP request
    return render(request, 'analytics/rawdata.html', context)



def pie_chart(request):



    # Get donation count for all donation categories
    
    # Funds
    funds_count = Fund.objects.all().count()

    # Giftcards
    giftscards_count = GiftCard.objects.all().count()

    # Clothing
    clothing_count = Clothing.objects.all().count()

    # Food
    food_count = Food.objects.all().count()

    # Miscellaneous
    misc_count = Miscellaneous.objects.all().count()

    context = {
        'funds': funds_count,
        'giftcards': giftscards_count,
        'clothing':clothing_count,
        'food': food_count,
        'miscellaneous': misc_count,
    }

    return render(request, 'analytics/piechart.html', context)