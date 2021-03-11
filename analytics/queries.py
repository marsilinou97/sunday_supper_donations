from django.db import models
from input.models import *
import sys  # debugging
from django.db import connection
from django.db.models import F
from analytics.vars import *
import functools
from itertools import chain
"""
Not sure if this is a good place to put this code, if you need to move it feel free. -Brad
"""

"""
Filters results. Just a quick implementation, there may be more efficient ways to do this,
but using this method means the db doesn't need to be queried every time the filter is changed.

Args:
    results: a list of dictionaries
    filters: a dictionary, where each key:value pair is searched for

Example:
    FilterResults(
                    results,
                    filters={"first_name":"John"}
                )

    This should strip the results of any
"""

#
# def FilterResults(
#         results,
#         filters={}
# ):
#     if filters != {}:
#         i = 0
#         while i < len(results):
#             removed = False
#             for key in filters:
#                 print(key)
#                 try:
#                     if not removed and results[i][key] != filters[key]:
#                         results.remove(results[i])
#                         removed = True
#                 except:
#                     print(sys.exc_info()[0])  # debugging
#                     print(sys.exc_info()[1])
#                     print(sys.exc_info()[2])
#             if not removed:
#                 i += 1
#     return results


# TODO: Enhance the caching, only store most recent N rows, update cache when adding/removing data
temp_caching = {}

"""
Query the db to get Funds that were donated and all relevant info
Returns a list of dictionaries with the following fields:
type, amount, quantity, date_received, first_name, last_name
"""


# def SelectAllFunds():
#     if "SelectAllFunds" in temp_caching.keys():
#         return temp_caching["SelectAllFunds"]
#     results = []
#     a = Fund.objects.all()
#     if a.exists():
#         for fund in a:
#             row = {}
#             row["type"] = fund.type.name
#             row["amount"] = fund.amount
#
#             # Not all of these try blocks are necessary; just in case.
#             try:
#                 b = Item.objects.get(id=fund.item.id)
#                 row["quantity"] = b.quantity
#             except:
#                 print("Item doesn't exist")
#             try:
#                 c = Donation.objects.get(id=b.donation.id)
#                 row["date_received"] = c.date_received
#             except:
#                 print("Donation doesn't exist")
#             try:
#                 d = Donor.objects.get(id=c.donor.id)
#                 row["first_name"] = d.first_name
#                 row["last_name"] = d.last_name
#             except:
#                 print("Donor doesn't exist")
#
#             results.append(row)
#         temp_caching["SelectAllFunds"] = results
#     return results


"""
Query the db to get GiftCards that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    business_name, amount, quantity, date_received, first_name, last_name
"""


# def SelectAllGiftCards():
#     if "SelectAllGiftCards" in temp_caching.keys():
#         return temp_caching["SelectAllGiftCards"]
#     results = []
#     a = GiftCard.objects.all()
#     if a.exists():
#         for giftcard in a:
#             row = {}
#             row["business_name"] = giftcard.business_name.name
#             row["amount"] = giftcard.amount
#
#             # Not all of these try blocks are necessary; just in case.
#             try:
#                 b = Item.objects.get(id=giftcard.item.id)
#                 row["quantity"] = b.quantity
#             except:
#                 print("Item doesn't exist")
#             try:
#                 c = Donation.objects.get(id=b.donation.id)
#                 row["date_received"] = c.date_received
#             except:
#                 print("Donation doesn't exist")
#             try:
#                 d = Donor.objects.get(id=c.donor.id)
#                 row["first_name"] = d.first_name
#                 row["last_name"] = d.last_name
#             except:
#                 print("Donor doesn't exist")
#
#             results.append(row)
#         temp_caching["SelectAllGiftCards"] = results
#     return results


"""
Query the db to get Clothings that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    type, quantity, date_received, first_name, last_name
"""


# def SelectAllClothings():
#     if "SelectAllClothings" in temp_caching.keys():
#         return temp_caching["SelectAllClothings"]
#     results = []
#     a = Clothing.objects.all()
#     if a.exists():
#         for clothing in a:
#             row = {}
#             row["type"] = clothing.type.name
#
#             # Not all of these try blocks are necessary; just in case.
#             try:
#                 b = Item.objects.get(id=clothing.item.id)
#                 row["quantity"] = b.quantity
#             except:
#                 print("Item doesn't exist")
#             try:
#                 c = Donation.objects.get(id=b.donation.id)
#                 row["date_received"] = c.date_received
#             except:
#                 print("Donation doesn't exist")
#             try:
#                 d = Donor.objects.get(id=c.donor.id)
#                 row["first_name"] = d.first_name
#                 row["last_name"] = d.last_name
#             except:
#                 print("Donor doesn't exist")
#
#             results.append(row)
#         temp_caching["SelectAllClothings"] = results
#     return results


"""
Query the db to get Food Items that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    name, quantity, date_received, first_name, last_name
"""


# def SelectAllFood():
#     if "SelectAllFood" in temp_caching.keys():
#         return temp_caching["SelectAllFood"]
#     results = []
#     a = Food.objects.all()
#     if a.exists():
#         for food in a:
#             row = {}
#             row["name"] = food.name
#
#             # Not all of these try blocks are necessary; just in case.
#             try:
#                 b = Item.objects.get(id=food.item.id)
#                 row["quantity"] = b.quantity
#             except:
#                 print("Item doesn't exist")
#             try:
#                 c = Donation.objects.get(id=b.donation.id)
#                 row["date_received"] = c.date_received
#             except:
#                 print("Donation doesn't exist")
#             try:
#                 d = Donor.objects.get(id=c.donor.id)
#                 row["first_name"] = d.first_name
#                 row["last_name"] = d.last_name
#             except:
#                 print("Donor doesn't exist")
#
#             results.append(row)
#         temp_caching["SelectAllFood"] = results
#     return results


"""
Query the db to get Miscellaneous Items that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    misc_name, quantity, date_received, first_name, last_name
"""


# def SelectAllMiscellaneous():
#     if "SelectAllMiscellaneous" in temp_caching.keys():
#         return temp_caching["SelectAllMiscellaneous"]
#     results = []
#     a = Miscellaneous.objects.all()
#     if a.exists():
#         for misc in a:
#             row = {}
#             row["misc_name"] = misc.name
#
#             # Not all of these try blocks are necessary; just in case.
#             try:
#                 b = Item.objects.get(id=misc.item.id)
#                 row["quantity"] = b.quantity
#             except:
#                 print("Item doesn't exist")
#             try:
#                 c = Donation.objects.get(id=b.donation.id)
#                 row["date_received"] = c.date_received
#             except:
#                 print("Donation doesn't exist")
#             try:
#                 d = Donor.objects.get(id=c.donor.id)
#                 row["first_name"] = d.first_name
#                 row["last_name"] = d.last_name
#             except:
#                 print("Donor doesn't exist")
#
#             results.append(row)
#         temp_caching["SelectAllMiscellaneous"] = results
#     return results


"""
Returns counts of all Item subclasses in the db. Accounts for quantity of each Item.
Return type is a dictionary.
"""

#
# def countItems():
#     counts = {}
#
#     try:
#         # Count each Item type
#         counts["funds"] = 0
#         for item in SelectAllFunds():
#             counts["funds"] += int(item["quantity"])
#
#         counts["giftcards"] = 0
#         for item in SelectAllGiftCards():
#             counts["giftcards"] += int(item["quantity"])
#
#         counts["clothing"] = 0
#         for item in SelectAllClothings():
#             counts["clothing"] += int(item["quantity"])
#
#         counts["food"] = 0
#         for item in SelectAllFood():
#             counts["food"] += int(item["quantity"])
#
#         counts["misc"] = 0
#         for item in SelectAllMiscellaneous():
#             counts["misc"] += int(item["quantity"])
#
#         # Sum them
#         counts["all"] = 0
#         for key in counts:
#             counts["all"] += counts[key]
#
#         # counts["all"] will be added to itself, so divide by 2 and cast as int to compensate
#         counts["all"] = int(counts["all"] / 2)
#     except:
#         for error in sys.exc_info():
#             print(error)
#     return counts


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
    
    #query = model.objects.prefetch_related('item').values("item__quantity")
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
