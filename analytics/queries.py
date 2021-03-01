from django.db import models
from input.models import *
import sys  # debugging

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


def FilterResults(
        results,
        filters={}
):
    if filters != {}:
        i = 0
        while i < len(results):
            removed = False
            for key in filters:
                try:
                    if not removed and results[i][key] != filters[key]:
                        results.remove(results[i])
                        removed = True
                except:
                    print(sys.exc_info()[0])  # debugging
                    print(sys.exc_info()[1])
                    print(sys.exc_info()[2])
            if not removed:
                i += 1
    return results


"""
Query the db to get Funds that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    type, amount, quantity, date_received, first_name, last_name
"""
# TODO: Enhance the caching, only store most recent N rows, update cache when adding/removing data
temp_caching = {}


def SelectAllFunds():
    if "SelectAllFunds" in temp_caching.keys():
        return temp_caching["SelectAllFunds"]
    results = []
    a = Fund.objects.all()
    if a.exists():
        for fund in a:
            row = {}
            row["type"] = fund.type.name
            row["amount"] = fund.amount

            # Not all of these try blocks are necessary; just in case.
            try:
                b = Item.objects.get(id=fund.item.id)
                row["quantity"] = b.quantity
            except:
                print("Item doesn't exist")
            try:
                c = Donation.objects.get(id=b.donation.id)
                row["date_received"] = str(c.date_received)
            except:
                print("Donation doesn't exist")
            try:
                d = Donor.objects.get(id=c.donor.id)
                print(d)
                row["first_name"] = d.first_name
                row["last_name"] = d.last_name
            except:
                print("Donor doesn't exist")

            results.append(row)
        temp_caching["SelectAllFunds"] = results
    return results


"""
Query the db to get GiftCards that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    business_name, amount, quantity, date_received, first_name, last_name
"""


def SelectAllGiftCards():
    if "SelectAllGiftCards" in temp_caching.keys():
        return temp_caching["SelectAllGiftCards"]
    results = []
    a = GiftCard.objects.all()
    if a.exists():
        for giftcard in a:
            row = {}
            row["business_name"] = giftcard.business_name.name
            row["amount"] = giftcard.amount

            # Not all of these try blocks are necessary; just in case.
            try:
                b = Item.objects.get(id=giftcard.item.id)
                row["quantity"] = b.quantity
            except:
                print("Item doesn't exist")
            try:
                c = Donation.objects.get(id=b.donation.id)
                row["date_received"] = str(c.date_received)
            except:
                print("Donation doesn't exist")
            try:
                d = Donor.objects.get(id=c.donor.id)
                print(d)
                row["first_name"] = d.first_name
                row["last_name"] = d.last_name
            except:
                print("Donor doesn't exist")

            results.append(row)
        temp_caching["SelectAllGiftCards"] = results
    return results


"""
Query the db to get Clothings that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    type, quantity, date_received, first_name, last_name
"""


def SelectAllClothings():
    if "SelectAllClothings" in temp_caching.keys():
        return temp_caching["SelectAllClothings"]
    results = []
    a = Clothing.objects.all()
    if a.exists():
        for clothing in a:
            row = {}
            row["type"] = clothing.type.name

            # Not all of these try blocks are necessary; just in case.
            try:
                b = Item.objects.get(id=clothing.item.id)
                row["quantity"] = b.quantity
            except:
                print("Item doesn't exist")
            try:
                c = Donation.objects.get(id=b.donation.id)
                row["date_received"] = str(c.date_received)
            except:
                print("Donation doesn't exist")
            try:
                d = Donor.objects.get(id=c.donor.id)
                print(d)
                row["first_name"] = d.first_name
                row["last_name"] = d.last_name
            except:
                print("Donor doesn't exist")

            results.append(row)
        temp_caching["SelectAllClothings"] = results
    return results


"""
Query the db to get Food Items that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    name, quantity, date_received, first_name, last_name
"""


def SelectAllFood():
    if "SelectAllFood" in temp_caching.keys():
        return temp_caching["SelectAllFood"]
    results = []
    a = Food.objects.all()
    if a.exists():
        for food in a:
            row = {}
            row["misc_name"] = food.name

            # Not all of these try blocks are necessary; just in case.
            try:
                b = Item.objects.get(id=food.item.id)
                row["quantity"] = b.quantity
            except:
                print("Item doesn't exist")
            try:
                c = Donation.objects.get(id=b.donation.id)
                row["date_received"] = str(c.date_received)
            except:
                print("Donation doesn't exist")
            try:
                d = Donor.objects.get(id=c.donor.id)
                print(d)
                row["first_name"] = d.first_name
                row["last_name"] = d.last_name
            except:
                print("Donor doesn't exist")

            results.append(row)
        temp_caching["SelectAllFood"] = results
    return results


"""
Query the db to get Miscellaneous Items that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    misc_name, quantity, date_received, first_name, last_name
"""


def SelectAllMiscellaneous():
    if "SelectAllMiscellaneous" in temp_caching.keys():
        return temp_caching["SelectAllMiscellaneous"]
    results = []
    a = Miscellaneous.objects.all()
    if a.exists():
        for misc in a:
            row = {}
            row["misc_name"] = misc.name

            # Not all of these try blocks are necessary; just in case.
            try:
                b = Item.objects.get(id=misc.item.id)
                row["quantity"] = b.quantity
            except:
                print("Item doesn't exist")
            try:
                c = Donation.objects.get(id=b.donation.id)
                row["date_received"] = str(c.date_received)
            except:
                print("Donation doesn't exist")
            try:
                d = Donor.objects.get(id=c.donor.id)
                print(d)
                row["first_name"] = d.first_name
                row["last_name"] = d.last_name
            except:
                print("Donor doesn't exist")

            results.append(row)
        temp_caching["SelectAllMiscellaneous"] = results
    return results
