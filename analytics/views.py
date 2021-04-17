import json
import traceback

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from helpers import FailedJsonResponse
from helpers import remove_html_tags
from input.forms import FundsForm, ItemForm
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


def edit_donations(request):
    # forms = {
    #     'donor_form': DonorInformationForm(),
    #     'donation_info_form': DonationForm(),
    #     'funds_form': FundsForm(),
    # }
    return render(request, 'analytics/edit_donations.html', {'funds_form_types': FundsForm(), 'item_form': ItemForm()})


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
    if request.method == "GET":

        json_response = {}
        for key in QUERY_DATA.keys():
            qty_count_by_month = [0 for _ in range(12)]

            list_of_data = list(get_quantity_group_by_date(QUERY_DATA[key]["MODEL"], "month"))

            for row in list_of_data:
                qty_count_by_month[row["month"] - 1] += row["qty"]

            json_response.update({
                key: qty_count_by_month
            })

        return JsonResponse(json_response, safe=False)


def get_donation_count_month(request):
    if request.method == "GET":

        json_response = {}
        for key in QUERY_DATA.keys():
            qty_count_by_month = [0 for _ in range(12)]

            list_of_data = list(get_donation_count_by_date(QUERY_DATA[key]["MODEL"], "month"))

            for row in list_of_data:
                qty_count_by_month[row["month"] - 1] += row["count"]

            json_response.update({
                key: qty_count_by_month
            })

        return JsonResponse(json_response, safe=False)


def get_donation_item_count(request):
    if request.method == "GET":

        json_response = {}
        for key in QUERY_DATA.keys():
            results = get_total_donation_count_qty(QUERY_DATA[key]["MODEL"])

            json_response.update({
                key: results["qty"]
            })

        return JsonResponse(json_response, safe=False)


def get_donation_fund_count(request):
    if request.method == "GET":

        fund_types = list(FundType.objects.all())
        json_response = {}
        for fund_type in fund_types:
            results = get_funds_count_qty(fund_type)
            print(fund_type.name)
            print(results)

            json_response.update({
                fund_type.name: results
            })

        return JsonResponse(results, safe=False)


# @login_required
def update_item(request):
    if request.method == "POST":
        try:
            ids = []
            update_data = json.loads(request.POST["update_data"])

            # Sanitize data
            for k, v in update_data.items():
                if type(v) not in (int, float, bool):
                    update_data[k] = remove_html_tags(v)

            print(update_data)
            ids.append(update_data["donor_id"])
            ids.append(update_data["donation_id"])
            ids.append(update_data["item_id"])
            ids.append(update_data["item_id"])
            res = update_item_entry(ids, update_data, request.POST["table_type"])
            if not res:
                res = {"error": "Couldn't update the" + request.POST["table_type"] + " entry, please try again."}
                return FailedJsonResponse(res)
            return JsonResponse(res, safe=False)

        except Exception as e:
            print(traceback.format_exc())
            print(f"The error is {e}")
            return FailedJsonResponse({"error": "Unexpected error occurred while updating data"})

    return FailedJsonResponse({"error": "Unknown method"})


def delete_item(request):
    # TODO sanitize data
    if request.method == "POST":
        try:
            item_id = request.POST["item_id"]
            model = QUERY_DATA[request.POST["table_type"]]["MODEL"]
            res = delete_item_entry(model, item_id)
            print(f"{item_id=}")

            if not res:
                res = {"error": "Couldn't update the" + request.POST["table_type"] + "entry, please try again."}
            print(f"{res=}")
            JsonResponse(res, safe=False)

        except Exception as e:
            print(f"The error is {e}")
            return HttpResponse("ERROR...")

    return HttpResponse("ERROR...")
