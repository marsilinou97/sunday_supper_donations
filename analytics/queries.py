from django.db import models
from input.models import *
import sys  # debugging
from django.db import connection

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

def execute_fetch_raw_query(query, fetch_all=False, fetch_one=False, params={}):
    if fetch_all or fetch_one:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_all:
                res = cursor.fetchall()
            if fetch_one:
                res = cursor.fetchone()
    return res

# @Ruben
TABLES_PKS = {
    "input_item":"id",
    "input_clothing":"item_id",
    "input_food":"item_id",
    "input_fund":"item_id",
    "input_giftcard":"item_id",
    "input_miscellaneous":"item_id",
    "input_donor":"id",
    "input_donation":"id"
}

"""
Executes at most 1 delete query per id in the ids argument.

args:
    table: name of the table to delete from
      ids: ids of entries to be deleted

Example call: execute_delete_query("input_item",["1","2","3"])
    This should generate the following query:
    DELETE FROM input_item WHERE id = %(id)s;

    And the following queries should be run:
    DELETE FROM input_item WHERE id = 1;
    DELETE FROM input_item WHERE id = 2;
    DELETE FROM input_item WHERE id = 3;

id might not have to be strings but i cast id as a string to be safe
"""
def execute_delete_query(table:str, ids:list):
    # Get the name of the pk column for that table
    try:
        column = TABLES_PKS[table]
    except KeyError as e:
        # If the table isn't in that dictionary then complain and exit
        print(e)
        return 0

    # This tuple represents the parts of the query that are shared between all parts of this query
    body = (
        "DELETE FROM ",
        " WHERE ",
        " = %(",
        ")s;"
    )
    count = 0

    # Start building the queries
    for id in ids:
        id = str(id)

        # Concatenate the body and the table and its pk
        query = body[0] + table + body[1] + column + body[2] + column + body[3]

        # Set up the one param for the query
        # I'm pretty sure the key needs to match the column name but I could be wrong.
        params = {column:id}

        # Try/catch is mostly just to be safe
        try:
            with connection.cursor() as cursor:
                cursor.execute(query,params)
                count += 1
        except:
            print("Couldn't delete")
    # probably not needed but might be useful
    print("Successfully deleted",count,"rows from",table)
    return count

"""
Executes at most m delete queries per element in tables.
args:
    tables: n x 1 matrix, consists of tables to be deleted from
       ids: n x m matrix, consists of lists of ids to be deleted
"""
def batch_delete(tables:list,ids:list):
    count = 0
    for i in range(len(tables)):
        count += execute_delete_query(tables[i],ids[i])
    print("Deleted",count,"rows from",len(tables),"tables")

"""
Executes at most 1 update query
args:
         table: name of the table
       columns: list of column names to be updated. MUST match the name of the column in the db
            id: used in the WHERE clause
    new_values: used in the SET clause. MUST be same length as columns, otherwise the query won't work
"""
def execute_update_query(table:str, id:str, columns:list, new_values:list):
    body = (
        "UPDATE ",
        " SET ",
        " WHERE ",
        " = %(",
        ")s;"
    )

    # Get the name of the pk column for this table
    pk = TABLES_PKS[table]
    i = 0 # iterator for values
    # Set up params dict
    params = {}
    params[pk] = id

    # Build UPDATE clause
    query = body[0] + table + body[1]

    # Build SET clause
    for column in columns:
        # Configure params
        params[column] = new_values[i]
        i += 1

        query = query + column + " = %(" + column + ")s"
        if column != columns[-1]:
            query = query + ", "

    # Build WHERE clause
    query = query + body[2] + pk + body[3] + pk + body[4]

    try:
        with connnection.cursor() as cursor:
            cursor.execute(query,params)
        return 1
    except:
        print("Couldn't update")
        return 0

"""
Executes at most 1 update query per element in tables.
args:
        tables: n x 1 matrix, consists of tables to update
           ids: n x 1 matrix, consists of ids to update
       columns: n x m matrix, consists of column names for all n queries
    new_values: n x m matrix, consists of values for all n queries

BE CAREFUL WITH THESE ARGS: they all must be the same length (n) in the first dimension,
and each columns[i] must be the same length (m) as each new_values[i] :) fun stuff
"""
def batch_update(tables:list, ids:list, columns:list, new_values:list):
    count = 0
    for i in range(len(tables)):
        count += execute_update_query(tables[i],ids[i],columns[i],new_values[i])
    print("Updated",count,"rows")
