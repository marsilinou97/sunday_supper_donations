from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import DonationForm, DonorInformationForm, FundsForm, ItemForm, Donor
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
import sys

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
    # Save the data that the user entered
    user_input = {}  # user input dictionary
    # user_input_items = {}  # items dictionary
    items_list = []  # list of dictionary for item types
    data = request.POST.dict()  # Get request.POST as a regular dictionary
    print(data)

    # Get information about Funds, if any were donated
    type = None
    amount = None
    send_thanks = False
    if "type" in data:
        type = data["type"]
    if "amount" in data:
        amount = data["amount"]
    if "thanks_sent" in data:
        if data["thanks_sent"] == "on":
            send_thanks = True

    # If there was a Fund donated, add it to the list
    if type != None and type != "" and amount != None:
        items_list.append({"subclass": Fund, "quantity": 1, "fundTypeName": type, "amount": amount})
    # Iterate over all item-related keys from request.POST
    i = 0
    next_key = 'id_form-' + str(i) + '-type'  # a.k.a.: 'id_form-' + str(i) + '-type'
    while next_key in data:
        """
        This loop condition should work for all items in the donation since all
        items will have the key 'id_form-' + str(i) + '-type'.
        """

        item_dict = {}
        item_dict['quantity'] = data['id_form-' + str(i) + '-quantity']

        # Get the Item subclass
        item_dict["subclass"] = data['id_form-' + str(i) + '-type']
        if item_dict['subclass'] == 'giftcard':
            item_dict['subclass'] = GiftCard
            item_dict['amount'] = data['id_form-' + str(i) + '-amount']  # TODO: fix once the form has an amount for Giftcards
            # get the Giftcard enumerated value
            if 'id_form-' + str(i) + '-sub_type_business' in data:
                item_dict['businessName'] = data['id_form-' + str(i) + '-sub_type_business']
            else:
                item_dict['businessName'] = ""

        elif item_dict['subclass'] == 'clothing':
            item_dict["subclass"] = Clothing
            # get the Clothing enumerated value
            if 'id_form-' + str(i-1) + '-sub_type_clothing' in data:
                item_dict['clothingTypeName'] = data['id_form-' + str(i-1) + '-sub_type_clothing']
            # else:
            #    item_dict['clothingTypeName'] = "men"

        elif item_dict['subclass'] == 'food':
            item_dict["subclass"] = Food

        elif item_dict['subclass'] == 'misc':
            item_dict["subclass"] = Miscellaneous

        if item_dict['subclass'] == Food or item_dict['subclass'] == Miscellaneous:
            # get the name of the Food/Misc
            if 'id_form-' + str(i) + '-sub_type_name' in data:
                item_dict['name'] = data['id_form-' + str(i) + '-sub_type_name']
            else:
                item_dict['name'] = ""

        # Add the item to the list
        items_list.append(item_dict)

        # Set up the next iteration
        i += 1
        next_key = 'id_form-' + str(i) + '-type'

    # Check if the donation was anonymous.
    donor = None
    if "anonymous" in user_input:
        if user_input['anonymous'] == 'on':
            # If it was, select the anonymous donor from the db
            donor = Donor.objects.get(first_name="ANONYMOUS", last_name="ANONYMOUS", email="")

    # If it wasn't anonymous, or if the anonymous donor wasn't in the db,
    # Try to insert the donor.
    if donor == None:
        # Get donor information from the POST request
        user_keys = ["first_name", "last_name", "email_address", "phone_number", "state",
                     "city", "zip", "address1", "address2"]
        for key in user_keys:
            # If the data exists, great. Use it
            if key in data:
                user_input[key] = data[key]
            # If the data doesn't exist, it stays blank.
            else:
                user_input[key] = ""

        # Now that we've doxxed the donor, try to insert them into the db
        try:
            donor = InsertDonor(user_input['first_name'], user_input['last_name'],
                                '', user_input['email_address'],
                                user_input['phone_number'],
                                user_input['address1'], user_input['address2'],
                                user_input['city'], user_input['state'],
                                user_input['zip'])
        except:
            for error in sys.exc_info():
                print(error)

    cur_user = User.objects.last()  # who is the current user
    # TODO: get the actual current user
    # if request.user.is_authenticated:  # authenticates the current user and can't be none
    #     cur_user = request.User.username
    # Now try to insert the donation. This should fail if donor == None
    # Should technically work even if items_list == []
    try:
        # InsertDonation(new_donor, items_list, user_input['date_received'], user_input['thanks_sent'], cur_user, "None")
        InsertDonation(donor, items_list, data['date_received'], send_thanks, cur_user, data['comment'])
    except:
        for error in sys.exc_info():
            print(error)

    """
    ===================================================================================================
        TEST CODE : Making sure that every value is in the right key.
    ===================================================================================================
    """
    print('date_received: ' + data['date_received'] + " |||| " )
    print('thanks_sent: ' + str(send_thanks) + " |||| ")
    print('comments: ' + data['comment'] + " |||| ")  # its comments on models.py
    print('type: ' + data['type'] + " ||||||| " + type)
    print('amount: ' + data['amount'] + " |||||||| " + amount)
    print('first_name: ' + data['first_name'] + " |||| " + user_input['first_name'])
    print('last_name: ' + data['last_name'] + " |||| " + user_input['last_name'])
    print('email: ' + data['email'] + " |||| " + user_input['email_address'])
    print('phone_number: ' + data['phone_number'] + " |||| " + user_input['phone_number'])
    print('address_line1: ' + data['address1'] + " |||| " + user_input['address1'])
    print('address_line2: ' + data['address2'] + " |||| " + user_input['address2'])
    print('city: ' + data['city'] + " |||| " + user_input['city'])
    # print('state: ' + data['state'] + " |||| ")
    # print('zipcode: ' + data['zip'] + " |||| " + user_input['zip'])

    messages.success(request, 'Donation Saved.')
    return redirect('input_page')

# @login_required
def index(request):
    if request.method == 'POST':
        return handle_post_req(request)

    elif request.method == 'GET':
        item_formset = formset_factory(ItemForm, extra=0)
        formset = item_formset()
        print(formset)
        # form set
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
