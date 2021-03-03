from django.shortcuts import render
from .forms import RawDataForm
from .queries import *
from input.models import *
from .vars import *
from django.shortcuts import redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'analytics/analytics.html')


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


def pie_chart(request):
    if request.method == 'GET':
        context = execute_fetch_raw_query(pie_chart_query, fetch_all=True)
        context = {k: v for k, v in context}
        context["all"] = sum(context.values())
        return render(request, 'analytics/piechart.html', context)
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
