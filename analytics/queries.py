from django.db import models
from input.models import *

"""
Not sure if this is a good place to put this code, if you need to move it feel free. -Brad
"""

"""
Query the db to get Funds that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    type, amount, quantity, date_received, first_name, last_name
"""
def SelectAllFunds():
    results = []
    a = Fund.objects.all()
    for fund in a:
        row = {}
        row["type"] = fund.type.name
        row["amount"] = fund.amount

        # Not all of these try blocks are necessary; just in case.
        try:
            b = Item.objects.get(id=fund.items_id.id)
            row["quantity"] = b.quantity
        except:
            print("Item doesn't exist")
        try:
            c = Donation.objects.get(id=b.donations_id.id)
            row["date_received"] = str(c.date_received)
        except:
            print("Donation doesn't exist")
        try:
            d = Donor.objects.get(id=c.donor.id)
            print(d)
        except:
            print("Donor doesn't exist")

        names = FindDonorNames(d)
        row["first_name"] = names[0]
        row["last_name"] = names[1]

        results.append(row)
    return results

"""
Query the db to get GiftCards that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    business_name, amount, quantity, date_received, first_name, last_name
"""
def SelectAllGiftCards():
    results = []
    a = GiftCard.objects.all()
    for giftcard in a:
        row = {}
        row["business_name"] = giftcard.business_name.name
        row["amount"] = giftcard.amount

        # Not all of these try blocks are necessary; just in case.
        try:
            b = Item.objects.get(id=giftcard.items_id.id)
            row["quantity"] = b.quantity
        except:
            print("Item doesn't exist")
        try:
            c = Donation.objects.get(id=b.donations_id.id)
            row["date_received"] = str(c.date_received)
        except:
            print("Donation doesn't exist")
        try:
            d = Donor.objects.get(id=c.donor.id)
            print(d)
        except:
            print("Donor doesn't exist")

        names = FindDonorNames(d)
        row["first_name"] = names[0]
        row["last_name"] = names[1]

        results.append(row)
    return results

"""
Query the db to get Clothings that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    type, quantity, date_received, first_name, last_name
"""
def SelectAllClothings():
    results = []
    a = Clothing.objects.all()
    for clothing in a:
        row = {}
        row["type"] = clothing.type.name

        # Not all of these try blocks are necessary; just in case.
        try:
            b = Item.objects.get(id=clothing.items_id.id)
            row["quantity"] = b.quantity
        except:
            print("Item doesn't exist")
        try:
            c = Donation.objects.get(id=b.donations_id.id)
            row["date_received"] = str(c.date_received)
        except:
            print("Donation doesn't exist")
        try:
            d = Donor.objects.get(id=c.donor.id)
            print(d)
        except:
            print("Donor doesn't exist")

        names = FindDonorNames(d)
        row["first_name"] = names[0]
        row["last_name"] = names[1]

        results.append(row)
    return results

"""
Query the db to get Miscellaneous Items that were donated and all relevant info
Returns a list of dictionaries with the following fields:
    misc_name, quantity, date_received, first_name, last_name
"""
def SelectAllMiscellaneous():
    results = []
    a = Miscellaneous.objects.all()
    for misc in a:
        row = {}
        row["misc_name"] = misc.name

        # Not all of these try blocks are necessary; just in case.
        try:
            b = Item.objects.get(id=misc.items_id.id)
            row["quantity"] = b.quantity
        except:
            print("Item doesn't exist")
        try:
            c = Donation.objects.get(id=b.donations_id.id)
            row["date_received"] = str(c.date_received)
        except:
            print("Donation doesn't exist")
        try:
            d = Donor.objects.get(id=c.donor.id)
            print(d)
        except:
            print("Donor doesn't exist")

        names = FindDonorNames(d)
        row["first_name"] = names[0]
        row["last_name"] = names[1]

        results.append(row)
    return results
