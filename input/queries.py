from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat

from input.models import Donor
from input.vars import SUB_TYPES

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

def get_subtypes_by_name(sub_type_name: str, order_by: bool = True, ascending : bool = True):
    query_set = SUB_TYPES[sub_type_name].objects.values()

    if order_by:
        if ascending:
            query_set.order_by("name")
        else:
            query_set.order_by("-name")

    return list(query_set)

def get_subtypes_for_choicefield(sub_type_name: str, order_by: bool = True, ascending : bool = True):
    query_set = get_subtypes_by_name(sub_type_name, order_by, ascending)
    for i in range(len(query_set)):
        name = query_set[i]['name']
        query_set[i] = (name, name)
    return query_set
