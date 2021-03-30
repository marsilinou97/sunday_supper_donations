from math import ceil
from typing import Dict
from django.db.models.query_utils import Q

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Extract
import datetime

from .forms import RawDataForm, ChartsForm

from .queries import *
from .vars import *

get_zeros_list = lambda n: [0] * n


def index(request):
    if request.method == 'GET':
        pie_context = get_pie_chart_context(pie_chart_query)
        context = get_line_chart_context(lines_charts_query)
        context.update(pie_context)

        form = ChartsForm()

        context.update({"form": form})

        cursor = connection.cursor()

        # Get all donation data for each chart
        cursor.execute(fund_chart_query)
        fund = dictfetchall(cursor)
        fund_data = {"fund_data": fund}

        cursor.execute(giftcard_chart_query)
        gift = dictfetchall(cursor)
        giftcard_data = {"giftcard_data": gift}

        cursor.execute(clothing_chart_query)
        cloth = dictfetchall(cursor)
        clothing_data = {"clothing_data": cloth}

        cursor.execute(food_chart_query)
        food = dictfetchall(cursor)
        food_data = {"food_data": food}

        cursor.execute(miscellaneous_chart_query)
        misc = dictfetchall(cursor)
        miscellaneous_data = {"miscellaneous_data": misc}

        context.update(fund_data)
        context.update(giftcard_data)
        context.update(clothing_data)
        context.update(food_data)
        context.update(miscellaneous_data)

        return render(request, 'analytics/analytics.html', context)

    elif request.method == 'POST':
        form = RawDataForm(request.POST)

        if form.is_valid():
            filters, pie_chart_filter_query = get_filters_and_query(form, pie_chart_query)
            filters, lines_chart_filter_query = get_filters_and_query(form, lines_charts_query)

            if not filters:
                # If no filters supplied redirect to the raw data page
                return redirect("analytics_rawdata")

            pie_context = get_pie_chart_context(pie_chart_filter_query)
            context = get_line_chart_context(lines_chart_filter_query)
            context.update(pie_context)

            form = RawDataForm()
            context.update({"form": form()})
            return render(request, 'analytics/analytics.html', context)

        else:
            HttpResponse("Error...")

def raw_data(request):
    form = RawDataForm()

    if request.method == 'GET':

        #tables_data = get_raw_page_tables_data(raw_data_query)
        context = {
            "form": form,
            "funds": tables_data['funds'],
            "clothing": tables_data['clothing'],
            "foods": tables_data['foods'],
            "giftcards": tables_data['giftcards'],
            "miscellaneous": tables_data['miscellaneous']
        }
        return render(request, 'analytics/rawdata.html', context)

    elif request.method == 'POST':
        # Handles POST request
        form = RawDataForm(request.POST)

        if form.is_valid():
            #filters, query_filter = get_filters_and_query(form, filter_query)

            if not filters:
                # If no filters supplied redirect to the raw data page
                return redirect("analytics_rawdata")

            #tables_data = get_raw_page_tables_data(query_filter, filters)

            context = {
                "form": form,
                "funds": tables_data['funds'],
                "clothing": tables_data['clothing'],
                "foods": tables_data['foods'],
                "giftcards": tables_data['giftcards'],
                "miscellaneous": tables_data['miscellaneous']
            }

        # Return populated context based on HTTP request
        return render(request, 'analytics/rawdata.html', context)
    else:
        HttpResponse("Error...")

        HttpResponse("Error...")

def delete_fund(request):
    fund_id = request.POST["fund_id"]
    print(fund_id)
    res = bool(Fund.objects.filter(item_id=fund_id).delete()[0])
    # res = 0
    if not res:
        res = {"error": "Couldn't delete the funds entry, please try again."}
    return JsonResponse(res, safe=False)

def edit_donations(request):
    return render(request, 'analytics/edit_donations.html')

def get_table(request):
    # Get request parse
    if request.method == "GET":
        try:
            model = request.GET["table_type"]
            offset = int(request.GET["offset"])
            limit = int(request.GET["limit"])

            query_info = QUERY_DATA[model]
            rows_count = query_info["MODEL"].objects.count()

            if model not in QUERY_DATA.keys():
                raise ValueError
            if limit < 0 or offset < 0:
                raise ValueError
            if offset > rows_count:
                raise ValueError

            query_set = get_model_raw_data_query(query_info["MODEL"], query_info["RAW_DATA_FIELDS"], offset, limit)
            json_response = {"rows": list(query_set), "total": query_info["MODEL"].objects.count()}

            return JsonResponse(json_response, safe=False)

        except Exception as e:
            print(f"The error is {e}")
            return HttpResponse("ERROR...")
    else:
        return HttpResponse("ERROR...")

def get_donation_count_date_qty(request):
    if (request.method == "GET"):
        
        json_response = {}
        for key in QUERY_DATA.keys():
            qty_count_by_month = [0 for i in range(12)]

            list_of_data = list(get_quantity_group_by_date(QUERY_DATA[key]["MODEL"], "month"))

            for row in list_of_data:
                qty_count_by_month[row["month"]-1] += row["qty"]
            
            json_response.update({
                key : qty_count_by_month
            })

        return JsonResponse(json_response, safe= False)

def get_donation_count_month(request):
    if (request.method == "GET"):
        
        json_response = {}
        for key in QUERY_DATA.keys():
            qty_count_by_month = [0 for i in range(12)]

            list_of_data = list(get_donation_count_by_date(QUERY_DATA[key]["MODEL"], "month"))

            for row in list_of_data:
                qty_count_by_month[row["month"]-1] += row["count"]
            
            json_response.update({
                key : qty_count_by_month
            })

        return JsonResponse(json_response, safe= False)

def get_donation_item_count(request):
    if (request.method == "GET"):
        
        json_response = {}
        for key in QUERY_DATA.keys():

            results = get_total_donation_count_qty(QUERY_DATA[key]["MODEL"])
            
            json_response.update({
                key : results["qty"]
            })

        return JsonResponse(json_response, safe= False)

def get_donation_fund_count(request):
    if (request.method == "GET"):
        
        fund_types = list(FundType.objects.all())
        json_response = {}
        for fund_type in fund_types:
            results = get_funds_count_qty(fund_type)
            print(fund_type.name)
            print(results)

            json_response.update({
                fund_type.name : results
            })


        return JsonResponse(results, safe= False)