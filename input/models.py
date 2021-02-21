from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Donor(models.Model):
    pass


class AnonymousDonor(models.Model):
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE, primary_key=True)


class IdentifiedDonor(models.Model):

    #Donor FK
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE, primary_key=True)


    date_of_birth = models.DateField()

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=11)

    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=13)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email_address


class Donation(models.Model):
    #Donor FK
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)

    # Users FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_received = models.DateField()
    thanks_sent = models.BooleanField()
    comments = models.TextField()

    def __str__(self):
        return self.donor + " " + self.date_received + " " + self.user









