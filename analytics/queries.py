from django.db import models
from django.db.models.aggregates import Count, Sum
from django.db.models.functions.datetime import Extract
from input.models import *
import sys  # debugging
from django.db import connection
from django.db.models import F, Q
from analytics.vars import *


def get_model_raw_data_query(model: models.Model, item_specific_fields: dict, offset: int, limit: int,
                             order_by_column: str = "", order_by_direction="", search_keyword: str = "", exact={}):
    try:
        select_fields = dict(RAW_DATA_BASE_FIELDS_KEYS)
        for key in item_specific_fields.keys():
            value = item_specific_fields[key]
            if value != 1:
                select_fields.update({key: value})

        fields_keys = list(RAW_DATA_BASE_FIELDS_KEYS.keys())
        fields_keys.extend(item_specific_fields.keys())

        query = model.objects.prefetch_related('item').annotate(
            **select_fields
        ).values(
            *fields_keys
        )

        if exact and exact.get("date_received_from", None) and exact.get("date_received_to", None):
            print("RANGE")
            print([exact.get("date_received_from"), exact.get("date_received_to")])
            query = query.filter(date_received__range=[exact.get("date_received_from"), exact.get("date_received_to")])
            del exact["date_received_from"]
            del exact["date_received_to"]

        if exact:
            query = query.filter(**exact)

        if search_keyword:
            print("**" * 100)
            print(f"{search_keyword=}")
            filters = Q(first_name__icontains=search_keyword) | \
                      Q(last_name__icontains=search_keyword) | \
                      Q(comments__icontains=search_keyword) | \
                      Q(sub_type__icontains=search_keyword)
            query = query.filter(filters)
            print(query.query)
        # MyClass.objects.filter(name__icontains=my_parameter)

        if order_by_column:
            # print("ORDER" * 100)
            if order_by_direction == "desc": order_by_column = "-" + order_by_column
            query = query.order_by(order_by_column)
        count = query.count()
        query = query[offset:offset + limit]
    except Exception as e:
        query = None
        count = 0
        print(e)
    return query, count


def get_quantity_group_by_date(model: models.Model, date_type: str):
    date = {
        date_type: Extract("item__donation__date_received", date_type)
    }

    query_set = model.objects \
        .annotate(**date) \
        .values(date_type) \
        .annotate(qty=Sum("item__quantity")) \
        .order_by()

    return query_set


def get_donation_count_by_date(model: models.Model, date_type: str):
    date = {
        date_type: Extract("item__donation__date_received", date_type)
    }

    query_set = model.objects \
        .annotate(**date) \
        .values(date_type) \
        .annotate(count=Count("*")) \
        .order_by()

    return query_set


def get_total_donation_count_qty(model: models.Model):
    query_set = model.objects \
        .aggregate(qty=Sum("item__quantity"))

    return query_set


def get_funds_count_qty(fund_type: FundType):
    query_set = Fund.objects \
        .filter(type=fund_type) \
        .aggregate(qty=Sum("item__quantity"))

    return query_set


def execute_fetch_raw_query(query, fetch_all=False, fetch_one=False, params={}):
    if fetch_all or fetch_one:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_all:
                res = cursor.fetchall()
            if fetch_one:
                res = cursor.fetchone()
    return res


def delete_item_entry(model: models.Model, id: int):
    success = (model.objects.filter(item_id=id).delete()[0] and
               Item.objects.filter(id=id).delete()[0])
    return success


def update_table_entry(model: models.Model, filters: dict, fields: dict):
    # return model.objects.filter(id=id).update(**feilds)[0]
    return model.objects.filter(**filters).update(**fields)


def update_item_entry(ids: list, data: dict, model_name: str):
    update_data = {}

    update_data.update({ids[0]: {key: data[key] for key in data.keys() if key in ('first_name', 'last_name')}})
    update_data.update({ids[1]: {key: data[key] for key in data.keys() if key in ('date_received', 'comments')}})
    update_data.update({ids[2]: {key: data[key] for key in data.keys() if key == 'quantity'}})
    print(update_data[ids[0]])
    print(f"{ids[2]=}")
    print(data)

    sub_item_fields = {}
    if model_name == "funds_table" or model_name == "giftcards_table":
        sub_item_fields.update({'amount': data['amount']})

    sub_item_fields.update({QUERY_DATA[model_name]["SUBTYPE_FIELD"]: data['sub_type']})

    r0 = update_table_entry(Donor, {"id": ids[0]}, update_data[ids[0]])
    r1 = update_table_entry(Donation, {"id": ids[1]}, update_data[ids[1]])
    r2 = update_table_entry(Item, {"id": ids[2]}, update_data[ids[2]])
    r3 = update_table_entry(QUERY_DATA[model_name]["MODEL"], {"item_id": ids[3]}, sub_item_fields)
    print(r0, r1, r2, r3)
    return r0 and r1 and r2 and r3
