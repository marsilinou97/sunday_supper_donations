from django.shortcuts import render
from .forms import RawDataForm
from .queries import *
from input.models import *


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