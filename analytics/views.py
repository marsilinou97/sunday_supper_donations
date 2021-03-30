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

        form = ChartsForm()

        context = {"form": form}

        return render(request, 'analytics/analytics.html', context)

    else:
        return HttpResponse("ERROR...")

def raw_data(request):
    if request.method == "GET":

        form = RawDataForm()

        context = {"form": form}


        return render(request, 'analytics/rawdata.html', context)

    else:
        return HttpResponse("ERROR...")

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
                key: qty_count_by_month
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
                key: qty_count_by_month
            })

        return JsonResponse(json_response, safe= False)

def get_donation_item_count(request):
    if (request.method == "GET"):
        
        json_response = {}
        for key in QUERY_DATA.keys():

            results = get_total_donation_count_qty(QUERY_DATA[key]["MODEL"])
            
            json_response.update({
                key: results["qty"]
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
                fund_type.name: results
            })


        return JsonResponse(results, safe= False)