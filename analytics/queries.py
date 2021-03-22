from django.db import models
from input.models import *
import sys  # debugging
from django.db import connection
from django.db.models import F
from analytics.vars import *

def get_model_raw_data_query(model: models.Model, item_specific_fields: dict, offset: int, limit: int):

    select_fields = dict(RAW_DATA_BASE_FIELDS_KEYS)
    select_fields.update(item_specific_fields)

    fields_keys = list(RAW_DATA_BASE_FIELDS_KEYS.keys())
    fields_keys.extend(item_specific_fields.keys())

    query = model.objects.prefetch_related('item').annotate(
        **select_fields
    ).values(
        *fields_keys
    )[offset:limit]
    
    return query


def execute_fetch_raw_query(query, fetch_all=False, fetch_one=False, params={}):
    if fetch_all or fetch_one:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_all:
                res = cursor.fetchall()
            if fetch_one:
                res = cursor.fetchone()
    return res

def delete_table_entry(model: models.Model, id: str):
    model.objects.filter(id=id).delete()

def update_table_entry(model: models.Model, feilds: dict):
    model.objects.filter(id=id).update(**feilds)
