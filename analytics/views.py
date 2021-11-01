import os
from math import ceil
from typing import Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.db.models.query_utils import Q

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Extract
import datetime
import json
import traceback
from helpers import FailedJsonResponse
from django.forms import ChoiceField

from helpers import FailedJsonResponse
from helpers import remove_html_tags
from input.models import Donor
from input.forms import FundsForm, FundsEditForm, ItemForm, DonorEditForm
from input.queries import get_donor_list_wo_anonymous
from .forms import RawDataForm, ChartsForm

from .queries import *
from .vars import *

from analytics.excel import export_tables_to_excel

get_zeros_list = lambda n: [0] * n

@permission_required('input.view_item')
@login_required()
def index(request):
    if request.method == 'GET':

        form = ChartsForm()

        context = {"form": form}

        return render(request, 'analytics/analytics.html', context)

    else:
        return HttpResponse("ERROR...")

@permission_required('input.view_item')
@login_required()
def raw_data(request):
    if request.method == "GET":

        form = RawDataForm()

        context = {"form": form}

        return render(request, 'analytics/rawdata.html', context)

    else:
        return HttpResponse("ERROR...")

@permission_required('input.change_item')
@login_required()
def edit_donations(request):
    context = {'funds_form_types': FundsEditForm(), 'item_form': ItemForm()}
    return render(request, 'analytics/edit_donations.html', context)

@permission_required('input.change_item')
@login_required()
def edit_donors(request):
    context = {'form': DonorEditForm()}
    return render(request, 'analytics/edit_donors.html', context)


@permission_required('input.change_item')
@login_required()
def edit_donors_get_table(request):
    json_response = {"rows": list(get_donor_list_wo_anonymous()), "total": Donor.objects.count() - 1}
    return JsonResponse(json_response, safe=False)


@permission_required('input.change_item')
@login_required()
def update_donor(request):
    if request.method == "POST":
        try:
            update_data = json.loads(request.POST["update_data"])
            # Sanitize data
            for k, v in update_data.items():
                if type(v) not in (int, float, bool):
                    update_data[k] = remove_html_tags(v)

            # print(update_data)
            id = update_data["id"]
            # update_data.pop("id") # Don't want to accidentally update the Donor's id
            with transaction.atomic():
                # print(id)
                result = update_table_entry(Donor, {"id": id}, update_data)
                if not result:
                    result = {"error": "Couldn't update the Donor entry, please try again"}
                    raise Exception("Some exception :(")
            return JsonResponse(result, safe=False)
        except Exception as e:
            print(traceback.format_exc())
            print(f"The error is {e}")
            return FailedJsonResponse({"error": "Unexpected error occurred while updating data"})

    return FailedJsonResponse({"error": "Unknown method"})


from wsgiref.util import FileWrapper
from django.http import HttpResponse


def download(request, filename="test.xls"):
    # TODO create the file and pass the path to the function
    export_tables_to_excel(json.loads(request.GET['data']))

    path = './temp_downloads/'+filename
    wrapper = FileWrapper(open(path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(path)
    response['Content-Length'] = os.path.getsize(path)
    return response

@permission_required('input.view_item')
@login_required()
def get_table(request):
    # Get request parse
    if request.method == "GET":
        try:
            """
                {
                    table_type:
                    offset:
                    limit:
                    sort:
                    order:
                    search:
                    exact: {
                        first_name:
                        last_name:
                    }
                    range:
                }
            """
            exact_search = request.GET.get("exact", None)
            # print(dict(request.GET))
            if not exact_search:
                model = request.GET["table_type"]
                offset = int(request.GET["offset"])
                limit = int(request.GET["limit"])
                order_by_column = request.GET["sort"]
                order_by_direction = request.GET["order"]
                search_keyword = request.GET["search"]
            else:
                request.GET = json.loads(request.GET["exact"])
                model = request.GET["table_type"]
                offset = int(request.GET["offset"])
                limit = int(request.GET["limit"])
                order_by_column = ""
                order_by_direction = "asc"
                search_keyword = ""

            query_info = QUERY_DATA[model]
            rows_count = query_info["MODEL"].objects.count()

            if model not in QUERY_DATA.keys():
                raise ValueError
            if request.GET.get("exact", ""):
                if limit < 0 or offset < 0:
                    raise ValueError
                if offset > rows_count:
                    raise ValueError
            exact = request.GET.get("exact", {})
            query_set, count = get_model_raw_data_query(query_info["MODEL"], query_info["RAW_DATA_FIELDS"], offset,
                                                        limit, order_by_column, order_by_direction, search_keyword,
                                                        exact)

            # TODO check if no search being performed to return total number of rows, other wise return len(results)
            json_response = {"rows": list(query_set), "total": count}
            # json_response = {"rows": list(query_set), "total": query_info["MODEL"].objects.count()}
            # json_response = {"rows": list(query_set), "total": len(list(query_set))}

            if not json_response["rows"]: json_response = {"total": 0, "rows": []}
            # print(json_response)
            return JsonResponse(json_response, safe=False)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(f"The error is {e}")
            return HttpResponse("ERROR...")
    else:
        return HttpResponse("ERROR...")

@permission_required('input.view_item')
@login_required()
def get_donation_count_date_qty(request):
    if (request.method == "GET"):

        year = request.GET["year"]

        json_response = {}
        for key in QUERY_DATA.keys():
            qty_count_by_month = [0 for i in range(12)]

            list_of_data = list(get_quantity_group_by_date(QUERY_DATA[key]["MODEL"], "month", year))

            for row in list_of_data:
                qty_count_by_month[row["month"] - 1] += row["qty"]

            json_response.update({
                key: qty_count_by_month
            })

        return JsonResponse(json_response, safe=False)

@permission_required('input.view_item')
@login_required()
def get_donation_count_month(request):
    if (request.method == "GET"):

        year = request.GET["year"]
        json_response = {}
        for key in QUERY_DATA.keys():
            qty_count_by_month = [0 for i in range(12)]

            list_of_data = list(get_donation_count_by_date(QUERY_DATA[key]["MODEL"], "month", year))

            for row in list_of_data:
                qty_count_by_month[row["month"] - 1] += row["count"]

            json_response.update({
                key: qty_count_by_month
            })

        return JsonResponse(json_response, safe=False)

@permission_required('input.view_item')
@login_required()
def get_donation_item_count(request):
    if (request.method == "GET"):
        year = request.GET["year"]

        json_response = {}
        for key in QUERY_DATA.keys():
            results = get_total_donation_count_qty(QUERY_DATA[key]["MODEL"], year)

            json_response.update({
                key: results["qty"]
            })

        return JsonResponse(json_response, safe=False)


# Removed
def get_donation_fund_count(request):
    if (request.method == "GET"):

        year = request.GET["year"]

        fund_types = list(FundType.objects.all())
        json_response = {}
        for fund_type in fund_types:
            results = get_funds_count_qty(fund_type, year)
            # print(fund_type.name)
            # print(results)

            json_response.update({
                fund_type.name: results
            })

        return JsonResponse(results, safe=False)
    return HttpResponse("ERROR...")


@permission_required('input.change_item')
@login_required()
def update_item(request):
    if request.method == "POST":
        try:
            ids = []
            update_data = json.loads(request.POST["update_data"])
            ids.append(update_data["donor_id"])
            ids.append(update_data["donation_id"])
            ids.append(update_data["item_id"])
            ids.append(update_data["item_id"])
            res = update_item_entry(ids, update_data, request.POST["table_type"])
            # print(res)
            if not res:
                res = {"error": "Couldn't update the" + request.POST["table_type"] + " entry, please try again."}
                return FailedJsonResponse(res)

            return JsonResponse(res, safe=False)

        except Exception as e:
            print(traceback.format_exc())
            print(f"The error is {e}")
            return HttpResponse("ERROR...")

    return HttpResponse("ERROR...")

@permission_required('input.change_item')
@login_required()
def delete_item(request):
    if (request.method == "POST"):
        try:
            id = request.POST["item_id"]
            model = QUERY_DATA[request.POST["table_type"]]["MODEL"]
            res = delete_item_entry(model, id)
            print(f"{id=}")

            if not res:
                res = {"error": "Couldn't update the" + request.POST["table_type"] + "entry, please try again."}
            print(f"{res=}")
            JsonResponse(res, safe=False)

        except Exception as e:
            print(f"The error is {e}")
            return HttpResponse("ERROR...")

    return HttpResponse("ERROR...")
