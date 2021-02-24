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
def AllFunds():
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

        # These next two try blocks ARE necessary; we don't know if the donor is anonymous yet.
        # A Model.DoesNotExist exception WILL be thrown by get() if get() returns nothing
        try:
            anon = AnonymousDonor.objects.get(pk=d)
            row["first_name"] = "ANONYMOUS"
            row["last_name"] = ""
        except:
            print("Not Anonymous")
            anon = None
        try:
            known = IdentifiedDonor.objects.get(pk=d)
            row["first_name"] = known.first_name
            row["last_name"] = known.last_name
        except:
            print("Anonymous")
            known = None

        # Just in case both donor try blocks catch exceptions:
        if anon == None and known == None:
            row["first_name"] = "NODONORS"
            row["last_name"] = "ERROR"

        results.append(row)
    return results
