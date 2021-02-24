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
        # TODO test donation prints "<Donation: DONOR 1900-01-01  >"; need a way to print donor's name, or anonymous
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
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE)
    type = models.ForeignKey(ClothingType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.items_id} {self.type}"


class Food(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.items_id} {self.name}"


class Fund(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE)
    type = models.ForeignKey(FundType, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.items_id} {self.type} {self.amount}"


class GiftCard(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE)
    business_name = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.items_id} {self.business_name} {self.amount}"


class Miscellaneous(models.Model):
    items_id = models.OneToOneField(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.items_id} {self.name}"

def tableDebug():
    x = [AnonymousDonor,IdentifiedDonor,Donor,Donation,Item,Fund,GiftCard,Clothing,Food,Miscellaneous,FundType,Business,ClothingType,User]
    for x1 in x:
        print(x1.objects.all())
