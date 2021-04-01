from input.models import Donor
from django.db import models
from django.db.models import F
from django.db.models import Q

def get_donor_list_wo_anonymous():
    return Donor.objects.filter(~Q(first_name="ANONYMOUS")).values()
    
