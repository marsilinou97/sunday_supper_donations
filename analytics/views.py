from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import RawDataForm
from .queries import *
from .vars import *

get_zeros_list = lambda n: [0] * n


def get_funds(request):
    r = get_raw_page_tables_data2()
    # page_number = request.GET["page"]
    return JsonResponse(r, safe=False)


def index(request):
    if request.method == 'GET':
        pie_context = get_pie_chart_context(pie_chart_query)
        context = get_line_chart_context(lines_charts_query)
        context.update(pie_context)

        form = RawDataForm()
        context.update({"form": form})

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
        tables_data = get_raw_page_tables_data(raw_data_query)
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
            filters, query_filter = get_filters_and_query(form, filter_query)

            if not filters:
                # If no filters supplied redirect to the raw data page
                return redirect("analytics_rawdata")

            tables_data = get_raw_page_tables_data(query_filter, filters)

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


def pie_chart(request):
    if request.method == 'GET':
        context = get_pie_chart_context()
        return render(request, 'analytics/piechart.html', context)
    else:
        HttpResponse("Error...")


# ---------- Contexts getters start
def get_line_chart_context(requested_query):
    res = execute_fetch_raw_query(query=requested_query, fetch_all=True)

    results = {'funds': [get_zeros_list(12), get_zeros_list(12)], 'food': [get_zeros_list(12), get_zeros_list(12)],
               'miscellaneous': [get_zeros_list(12), get_zeros_list(12)],
               'clothing': [get_zeros_list(12), get_zeros_list(12)],
               'gifcards': [get_zeros_list(12), get_zeros_list(12)]}

    for item_type, month, number_of_donations, total_quantity in res:
        month = month.strip()
        results[item_type][0][INDEXED_MONTHS[month]] = results[item_type][0][INDEXED_MONTHS[month]] + total_quantity
        results[item_type][1][INDEXED_MONTHS[month]] = results[item_type][1][
                                                           INDEXED_MONTHS[month]] + number_of_donations
    return {"line_chart_context": results}


def get_pie_chart_context(requested_query):
    # print(requested_query)
    context = execute_fetch_raw_query(query=requested_query, fetch_all=True)
    # print(context)
    context = {k: v for k, v in context}
    context["all"] = sum(context.values())
    return context


# ---------- Contexts getters end

def line_chart(request):
    # TODO: 1.) Create form for linechart.html
    # TODO: 2.) Run queries based on donor information passed in from the line chart form
    # TODO: 3.) Pass context with donor data to linechart.html
    # TODO: 4.) Render data passed in from context in the linechart.html template
    if request.method == 'GET':
        context = get_line_chart_context()
        return render(request, 'analytics/linechart.html', context)
    else:
        HttpResponse("Error...")


def get_filters_and_query(form, query):
    filters = {}
    temp_filter_query = query + " WHERE "
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    donation_date_from = form.cleaned_data['donation_date_from']
    donation_date_to = form.cleaned_data['donation_date_to']

    if first_name:
        filters["first_name"] = first_name
        temp_filter_query += f" first_name ILIKE %(first_name)s AND "
    if last_name:
        filters["last_name"] = last_name
        temp_filter_query += f" last_name ILIKE %(last_name)s AND "
    if donation_date_from and donation_date_to:
        filters["date_received_from"] = donation_date_from
        filters["date_received_to"] = donation_date_to
        temp_filter_query += f" date_received BETWEEN %(date_received_from)s AND %(date_received_to)s  AND "
    elif donation_date_from:
        filters["date_received_from"] = donation_date_from
        filters["date_received_to"] = donation_date_from
        temp_filter_query += f" date_received BETWEEN %(date_received_from)s AND %(date_received_to)s  AND "
    temp_filter_query = temp_filter_query[:-4] + " ORDER BY date_received DESC "
    return filters, temp_filter_query


def get_raw_page_tables_data(query, params={}):
    results = {'funds': [], 'clothing': [], 'foods': [], 'giftcards': [], 'miscellaneous': []}
    res = execute_fetch_raw_query(query, fetch_all=True, params=params)
    for r in res:
        row_type = r[0]
        results[row_type].append(dict(zip(table_headers[row_type], r[1:])))
    return results


# c = []

def get_raw_page_tables_data2():
    # global c
    # if c: return c
    r = execute_fetch_raw_query(raw_data_query2, fetch_all=True)
    r_json = []
    # print(r)
    headers = list(table_headers['funds'])
    headers.insert(0, "id")
    for e in r:
        r_json.append(dict(zip(headers, e[1:])))
    # c = r_json
    # print(c)
    return r_json * 5


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
