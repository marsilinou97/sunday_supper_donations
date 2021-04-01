from django.db import models
from django.db.models.aggregates import Count, Sum
from django.db.models.functions.datetime import Extract
from input.models import *
import sys  # debugging
from django.db import connection
from django.db.models import F
from analytics.vars import *


def get_model_raw_data_query(model: models.Model, item_specific_fields: dict, offset: int, limit: int):
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
        )[offset:offset+limit]
    except Exception as e:
        query = None
        print(e)
    return query

def get_quantity_group_by_date(model: models.Model, date_type: str):
    date = {
        date_type: Extract("item__donation__date_received", date_type)
    }

    query_set = model.objects \
            .annotate(**date) \
            .values(date_type) \
            .annotate(qty = Sum("item__quantity")) \
            .order_by()

    return query_set

def get_donation_count_by_date(model: models.Model, date_type: str):
    date = {
        date_type: Extract("item__donation__date_received", date_type)
    }

    query_set = model.objects \
            .annotate(**date) \
            .values(date_type) \
            .annotate(count = Count("*")) \
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
    model.objects.filter(id=id).delete()
    Item.objects.filter(id=id).delete()

def update_item_entry(model: models.Model, id: int, feilds: dict):
    model.objects.filter(id=id).update(**feilds)
