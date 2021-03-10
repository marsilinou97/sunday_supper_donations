from django.shortcuts import render, redirect
from .forms import DonationForm, DonorInformationForm, FundsForm, ItemForm
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Donor, InsertDonor

us_states = {
    'Alabama': 'al', 'Alaska': 'ak', 'American Samoa': 'as', 'Arizona': 'az', 'Arkansas': 'ar', 'California': 'ca',
    'Colorado': 'co', 'Connecticut': 'ct', 'Delaware': 'de', 'District of Columbia': 'dc', 'Florida': 'fl',
    'Georgia': 'ga', 'Guam': 'gu', 'Hawaii': 'hi', 'Idaho': 'id', 'Illinois': 'il', 'Indiana': 'in', 'Iowa': 'ia',
    'Kansas': 'ks', 'Kentucky': 'ky', 'Louisiana': 'la', 'Maine': 'me', 'Maryland': 'md', 'Massachusetts': 'ma',
    'Michigan': 'mi', 'Minnesota': 'mn', 'Mississippi': 'ms', 'Missouri': 'mo', 'Montana': 'mt', 'Nebraska': 'ne',
    'Nevada': 'nv', 'New Hampshire': 'nh', 'New Jersey': 'nj', 'New Mexico': 'nm', 'New York': 'ny',
    'North Carolina': 'nc', 'North Dakota': 'nd', 'Northern Mariana Islands': 'mp', 'Ohio': 'oh', 'Oklahoma': 'ok',
    'Oregon': 'or', 'Pennsylvania': 'pa', 'Puerto Rico': 'pr', 'Rhode Island': 'ri', 'South Carolina': 'sc',
    'South Dakota': 'sd', 'Tennessee': 'tn', 'Texas': 'tx', 'Utah': 'ut', 'Vermont': 'vt', 'Virgin Islands': 'vi',
    'Virginia': 'va', 'Washington': 'wa', 'West Virginia': 'wv', 'Wisconsin': 'wi', 'Wyoming': 'wy'}


# Create your views here.
# 2 following def is for DonorInformationForm.
def handle_get_req(request):
    form = DonorInformationForm()
    return render(request, 'input/donor-info-form.html', {'form': form})


def handle_post_req(request):
    dic = {}
    # __id__ = ""
    # donationDic = {}  #  'date_received', 'comment', 'amount'
    # donorDic = {}     # 'first_name', 'last_name', 'email','dob', 'address1', 'address2', 'city', 'state', 'zip',
    # itemDic = {}      # 'type', 'quantity'

    for a in request.POST:
        dic[a] = request.POST[a]

    newDonor = InsertDonor(dic['first_name'], dic['last_name'], dic['dob'], dic['email'],
                           ' ', dic['address1'], dic['address2'], dic['city'], dic['state'],
                           dic['zip'])
    newDonor.save()

    """
    newDonation = DonationForm(dic['date_received'], dic['thanks_sent'], dic['comment'])
    if newDonation.is_valid():
        newDonation.save()
    else:
        return redirect('input_page')

    if a is "csrfmiddlewaretoken":
        __id__ = request.POST[a]
    elif a is "date_received" or "comment" or "thanks_sent":
        donationDic[a] = request.POST[a]
    elif a is "first_name" or "last_name" or "email" or "dob" or "address1" or "address2" or "city" or "state" or "zip":
        donorDic[a] = request.POST[a]
    else:
        itemDic[a] = request.POST[a]
    """

    """
    donation_form = DonationForm()
    if donation_form.is_valid():
        donation_form.save()
    else:
        return redirect('input_page')
    """

    """
    donation_form = DonationForm(request.POST, request.FILES)
    funds_form = FundsForm(request.POST, request.FILES)
    item_form = ItemForm(request.POST, request.FILES)

    if donor_information_form.is_valid() and donation_form.is_valid() and item_form.is_valid() and funds_form.is_valid():
        donor_information_form.save()
        donor_pk = donor_information_form.save()  # saving donor pk
        donation_form.instance.donor = donor_pk  # connects to donations

        donation_form_pk = donation_form.save()  # saving donation
        item_form.instance.donation = donation_form_pk  # connects to Items

        item_form_pk = item_form.save()  # saving the item

        funds_form.instance.item = item_form_pk  # map funds with items
        funds_form.instance.item.save()

        messages.success(request, "Information is saved on the database")
    else:
        messages.error(request, "Error 1: Invalid Input")
    """

# @login_required
def index(request):
    if request.method == 'POST':
        return handle_post_req(request)

    elif request.method == 'GET':
        item_formset = formset_factory(ItemForm, extra=0)
        formset = item_formset()
        print(formset)
        return render(request, 'input/donor-info-form.html',
                      {
                          'donor_form': DonorInformationForm(),
                          'donation_info_form': DonationForm(),
                          'funds_form': FundsForm(),
                          'item_form': ItemForm(),
                          'states': us_states,
                          'item_formset': formset
                      })
    else:
        messages.error(request, "Error")
        pass
