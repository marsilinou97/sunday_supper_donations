from django.db import models
from django.contrib.auth.models import User

# Django models documentation: https://docs.djangoproject.com/en/3.1/topics/db/models/


"""
Donor superclass
"""


class Donor(models.Model):
    def __str__(self):
        return f"{self.pk}"
    pass


"""
Donor subclasses
"""


class AnonymousDonor(models.Model):
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.pk} Anonymous"

class IdentifiedDonor(models.Model):
    # Donors FK
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE, primary_key=True)

    date_of_birth = models.DateField(blank=True, null=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email_address = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    address_line1 = models.CharField(max_length=50, blank=True, null=True)
    address_line2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=13, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} {self.email_address}"


"""
Donations
"""


class Donation(models.Model):
    # Donors FK
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)

    # Users FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_received = models.DateField()
    thanks_sent = models.BooleanField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.donor} {self.date_received}  {self.user}"


"""
Items
"""


class Item(models.Model):
    # Auto generated pk
    donations_id = models.ForeignKey(Donation, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.donations_id} {self.quantity}"


"""
Enumerations for Item subclasses
"""


class Business(models.Model):
    # Enumeration for GiftCards table; see Giftcard
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return f"{self.name}"


class ClothingType(models.Model):
    # Enumeration for Clothing table; see Clothing
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return f"{self.name}"


class FundType(models.Model):
    # Enumeration for Funds table
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return f"{self.name}"


"""
Item subclasses
"""


class Clothing(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    type = models.ForeignKey(ClothingType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.items_id} {self.type}"


class Food(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.items_id} {self.name}"


class Fund(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    type = models.ForeignKey(FundType, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.items_id} {self.type} {self.amount}"


class GiftCard(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    business_name = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.items_id} {self.business_name} {self.amount}"


class Miscellaneous(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.items_id} {self.name}"

"""
Debug function; prints all rows in all tables
"""
def tableDebug():
    x = [AnonymousDonor,IdentifiedDonor,Donor,Donation,Item,Fund,GiftCard,Clothing,Food,Miscellaneous,FundType,Business,ClothingType,User]
    for x1 in x:
        print(x1.objects.all())

"""
Helper function for queries that returns a list containing a donor's first and last names.
"""
def FindDonorNames(donor):
    anon = None
    known = None

    """
    These two try blocks ARE necessary; we don't know if the donor is anonymous yet.
    A Model.DoesNotExist exception WILL be thrown by get() if get() returns nothing,
    so it's expected that an exception will be raised in one of the two try blocks.
    """
    try:
        anon = AnonymousDonor.objects.get(pk=donor)
        first_name = "ANONYMOUS"
        last_name = ""
    except:
        print("Not Anonymous")
    try:
        known = IdentifiedDonor.objects.get(pk=donor)
        first_name = known.first_name
        last_name = known.last_name
    except:
        print("Anonymous")

    # Just in case both donor try blocks catch exceptions:
    if anon == None and known == None:
        first_name = "NODONORS"
        last_name = "ERROR"
    return [first_name,last_name]

"""
Helper function for queries that returns a donor with a matching first and last names.
TODO uniqueness
"""
def FindDonor(first_name,last_name):
    them = IdentifiedDonor.objects.filter(first_name=first_name,last_name=last_name)
    donor = Donor.objects.get(id=them.donor.id)
    return donor

"""
Insert a Donor into the table for IdentifiedDonors. Checks for uniqueness before insertion.
"""
def InsertDonor(
                first_name, # Required
                last_name,
                date_of_birth = None, # Optional
                email_address = None,
                phone_number = None,
                address_line1 = None,
                address_line2 = None,
                city = None,
                state = None,
                zipcode = None
                ):

    donor = None
    """
    Query IdentifiedDonor table for any matches; if the resulting queryset is empty,
    we can create the next one.

    If we need to add more uniqueness constraints that's fine, add them after the
    last_name argument.
    """
    donors = IdentifiedDonor.objects.filter(
                                            first_name=first_name,
                                            last_name=last_name
                                            )
    if len(donors) == 0:
        """
        Get the next id for the new donor. As far as I can tell, we don't have
        a way to get django to do this for us in this case, since the pk for
        IdentifiedDonor is a OneToOneField object, not an AutoField object.
        Maybe there's a way to extend both of those classes, but I don't think we
        know enough to do that right now.
        https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.OneToOneField
        https://docs.djangoproject.com/en/3.1/topics/db/models/#automatic-primary-key-fields
        -Brad
        """
        nextId = Donor.objects.last().id
        nextId += 1
        donor = Donor(nextId)
        donor.save()

        # Build and save the IdentifiedDonor
        them = IdentifiedDonor()
        them.donor = donor
        them.first_name = first_name
        them.last_name = last_name
        them.email_address = email_address
        them.phone_number = phone_number
        them.address_line1 = address_line1
        them.address_line2 = address_line2
        them.city = city
        them.state = state
        them.zipcode = zipcode
        them.save()
        print(them,"created")
    else:
        print("Donor",first_name,last_name,"already exists")
    return donor

"""
Insert a Donation into the table for Donations. Also calls InsertItem(). The argument
items cannot be the empty list. It is safe to call this with the empty list, though.
The items arg should be a list of dictionaries with arguments that correspond to
InsertItem() (with the exception of the donation id, which is produced before any
calls to InsertItem()).
"""
def InsertDonation(
                    donor,
                    date_received=None,
                    thanks_sent=None,
                    user=None,
                    comments=None,
                    items=[]
                    ):
    if len(items) == 0:
        print("Donations need an item")
    else:
        # Set up the Donation
        donation = Donation()
        donation.donor = donor
        donation.date_received = date_received
        donation.thanks_sent = thanks_sent
        donation.user = user
        donation.comments = comments
        donation.save()

        # Add the Items
        count = 0
        for item in items:
            try:
                InsertItem(
                            donation.id,
                            item["quantity"],
                            item["subclass"], # this name can probably be changed if needed
                            item["type"],
                            item["amount"],
                            item["name"],
                            item["fundTypeName"],
                            item["businessName"],
                            item["clothingTypeName"],
                            )
                count += 1
            except:
                print("Could not insert Item")
        print("Inserted",count,"items")

"""
Insert an Item into the table for Items and an instance of the appropriate subclass
into its corresponding table. The subclass arg is required. Other args are required
depending on the subclass you use when calling.

Usage:
    InsertItem(
                donation.donations_id,
                "1",
                Fund,
                amount="20",
                fundTypeName="Check",     # if you insert Fund, fundTypeName is required
                )
"""

def InsertItem(
                donations_id, # Required
                quantity,
                subclass,
                type=None, # Optional
                amount=None,
                name=None,
                fundTypeName=None,
                businessName=None,
                clothingTypeName=None,
                ):
    subclasses = [Fund,GiftCard,Clothing,Food,Miscellaneous]
    if subclass in subclasses:
        item = Item()
        item.donations_id = donations_id
        item.quantity = quantity
        item.save()
        if subclass == Fund:
            fund = Fund()
            fund.items_id = item
            fund.type = FundType().objects.get(name=FundTypeName)
            fund.amount = amount
            fund.save()
        elif subclass == GiftCard:
            giftcard = GiftCard()
            giftcard.items_id = item
            giftcard.business_name = Business().objects.get(name=businessName)
            giftcard.amount = amount
            giftcard.save()
        elif subclass == Clothing:
            clothing = Clothing()
            clothing.items_id = item
            clothing.type = ClothingType().objects.get(name=clothingTypeName)
            clothing.save()
        elif subclass == Food:
            food = Food()
            food.items_id = item
            food.name = name
            food.save()
        elif subclass == Miscellaneous:
            misc = Miscellaneous()
            misc.items_id = item
            misc.name = name
            misc.save()
    else:
        print("Item subclass not recognized")
