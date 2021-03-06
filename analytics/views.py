from django.shortcuts import render
from .forms import RawDataForm
from .queries import *
from input.models import *
from .vars import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import Template, Context


def index(request):
    # render(request, 'analytics/number_of_donations_per_month.html', {'results': results})
    pie_context = get_pie_chart_context()
    context = {"results": get_line_chart_data()}
    context.update(pie_context)
    return render(request, 'analytics/analytics.html', context)


def raw_data(request):
    form = RawDataForm()

    if request.method == 'GET':
        tables_data = get_tables_data(raw_data_query)
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
            filters, query_filter = get_filters_and_query(form)

            if not filters:
                # If no filters supplied redirect to the raw data page
                return redirect("analytics_rawdata")

            tables_data = get_tables_data(query_filter, filters)

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


def get_pie_chart_context():
    context = execute_fetch_raw_query(pie_chart_query, fetch_all=True)
    context = {k: v for k, v in context}
    context["all"] = sum(context.values())
    return context


def pie_chart(request):
    if request.method == 'GET':
        context = get_pie_chart_context()
        return render(request, 'analytics/piechart.html', context)
    else:
        HttpResponse("Error...")


get_zeros_list = lambda n: [0 for _ in range(n)]


def get_line_chart_data():
    q = """SELECT 'funds', to_char(date_received, 'Month') AS monnth, count(*) number_of_donations, sum(quantity) AS quantity FROM input_fund f INNER JOIN input_item ii ON f.item_id = ii.id INNER JOIN input_donation i ON ii.donation_id = i.id GROUP BY monnth UNION ALL SELECT 'food', to_char(date_received, 'Month') AS monnth, count(*) number_of_donations, sum(quantity) AS quantity FROM input_food f INNER JOIN input_item ii ON f.item_id = ii.id INNER JOIN input_donation i ON ii.donation_id = i.id GROUP BY monnth UNION ALL SELECT 'miscellaneous', to_char(date_received, 'Month') AS monnth, count(*)                           number_of_donations, sum(quantity)                   AS quantity FROM input_miscellaneous f INNER JOIN input_item ii ON f.item_id = ii.id INNER JOIN input_donation i ON ii.donation_id = i.id GROUP BY monnth UNION ALL SELECT 'clothing', to_char(date_received, 'Month') AS monnth, count(*)                           number_of_donations, sum(quantity)                   AS quantity FROM input_clothing f INNER JOIN input_item ii ON f.item_id = ii.id INNER JOIN input_donation i ON ii.donation_id = i.id GROUP BY monnth UNION ALL SELECT 'gifcards', to_char(date_received, 'Month') AS monnth, count(*)                           number_of_donations, sum(quantity)                   AS quantity FROM input_giftcard f INNER JOIN input_item ii ON f.item_id = ii.id INNER JOIN input_donation i ON ii.donation_id = i.id GROUP BY monnth  ORDER BY 1"""
    res = execute_fetch_raw_query(query=q, fetch_all=True)

    results = {'funds': [get_zeros_list(12), get_zeros_list(12)], 'food': [get_zeros_list(12), get_zeros_list(12)],
               'miscellaneous': [get_zeros_list(12), get_zeros_list(12)],
               'clothing': [get_zeros_list(12), get_zeros_list(12)],
               'gifcards': [get_zeros_list(12), get_zeros_list(12)]}

    for item_type, month, number_of_donations, total_quantity in res:
        month = month.strip()
        results[item_type][0][INDEXED_MONTHS[month]] = results[item_type][0][INDEXED_MONTHS[month]] + total_quantity
        results[item_type][1][INDEXED_MONTHS[month]] = results[item_type][1][
                                                           INDEXED_MONTHS[month]] + number_of_donations
    return results


def line_chart(request):
    # TODO: 1.) Create form for linechart.html
    # TODO: 2.) Run queries based on donor information passed in from the line chart form
    # TODO: 3.) Pass context with donor data to linechart.html
    # TODO: 4.) Render data passed in from context in the linechart.html template
    if request.method == 'GET':
        results = get_line_chart_data()
        return render(request, 'analytics/linechart.html', {'results': results})
    else:
        HttpResponse("Error...")


def get_filters_and_query(form):
    filters = {}
    temp_filter_query = filter_query
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


def get_tables_data(query, params={}):
    results = {'funds': [], 'clothing': [], 'foods': [], 'giftcards': [], 'miscellaneous': []}
    res = execute_fetch_raw_query(query, fetch_all=True, params=params)
    for r in res:
        row_type = r[0]
        results[row_type].append(dict(zip(table_headers[row_type], r[1:])))
    return results
