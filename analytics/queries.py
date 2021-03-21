from django.db import models
from input.models import *
import sys  # debugging
from django.db import connection
from django.db.models import F
from analytics.vars import *

def get_model_raw_data_query(model: models.Model, item_specific_fields: dict):

    select_fields = dict(RAW_DATA_BASE_FIELDS_KEYS)
    select_fields.update(item_specific_fields)

    fields_keys = list(RAW_DATA_BASE_FIELDS_KEYS.keys())
    fields_keys.extend(item_specific_fields.keys())

    query = model.objects.prefetch_related('item').annotate(
        **select_fields
    ).values(
        *fields_keys
    )
    
    return query

def union_queries(list_of_queries: list):
    return  list_of_queries[0].union(*list_of_queries[1:], all=True)

def get_raw_data_query():
    queries = []
    for query in RAW_DATA_QUERIES:
        queries.append(get_model_raw_data_query(
            query["MODEL"],
            query["FIELDS"]
        ))
    return union_queries(queries) 


def execute_fetch_raw_query(query, fetch_all=False, fetch_one=False, params={}):
    if fetch_all or fetch_one:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_all:
                res = cursor.fetchall()
            if fetch_one:
                res = cursor.fetchone()
    return res
