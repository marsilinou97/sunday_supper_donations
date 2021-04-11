from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat

from input.models import Donor


def get_donor_list_wo_anonymous():
    return Donor.objects.filter(~Q(first_name="ANONYMOUS")).values()


# Search first and last name
def get_donors_w_name(term):
    return Donor.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(
        full_name__icontains=term).values()


def get_donors_w_first_nm(term):
    return Donor.objects.filter(Q(first_name__icontains=term) & ~Q(first_name__contains="ANONYMOUS")).values()


def get_donors_w_last_nm(term):
    return Donor.objects.filter(Q(last_name__icontains=term) & ~Q(last_name__contains="ANONYMOUS")).values()
