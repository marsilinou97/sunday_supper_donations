import bleach
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.forms import formset_factory
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import json

from input.queries import get_donor_list_wo_anonymous, get_donors_w_first_nm, get_donors_w_last_nm, get_subtypes_by_name
from .forms import DonationForm, DonorInformationForm, FundsForm, ItemForm, BusinessForm, BusinessEditForm
from .models import *
from analytics.queries import update_table_entry

us_states = {
    '':'', 'California': 'ca', 'Alabama': 'al', 'Alaska': 'ak', 'American Samoa': 'as', 'Arizona': 'az', 'Arkansas': 'ar',
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
    items_list = []  # list of dictionary for item types
    data = request.POST.dict()  # Get request.POST as a regular dictionary

    # Handle the case where the state is unknown
    if "state" not in data:
        data["state"] = ""

    print(data)  # debug

    # Get information about Funds, if any were donated
    type = None
    amount = None
    if "type" in data:
        type = data["type"]
    if "amount" in data:
        amount = data["amount"]

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
            item_dict['amount'] = data[
                'id_form-' + str(i) + '-amount']  # TODO: fix once the form has an amount for Giftcards
            # get the Giftcard enumerated value
            if 'id_form-' + str(i) + '-sub_type_business' in data:
                item_dict['businessName'] = data['id_form-' + str(i) + '-sub_type_business']
            else:
                item_dict['businessName'] = ""

        elif item_dict['subclass'] == 'clothing':
            item_dict["subclass"] = Clothing
            # get the Clothing enumerated value
            if 'id_form-' + str(i) + '-sub_type_clothing' in data:
                item_dict['clothingTypeName'] = data['id_form-' + str(i) + '-sub_type_clothing']

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

    if save_donation(items_list, data) is False:
        print("Donation not saved")
    else:
        messages.success(request, 'Donation Saved.')

    return redirect('input_index')


def save_donation(items_list, data):
    donation_saved = False
    user_input = {}  # user input dictionary

    cur_user = User.objects.last()  # who is the current user
    # TODO: get the actual current user
    # if request.user.is_authenticated:  # authenticates the current user and can't be none
    #     cur_user = request.User.username

    send_thanks = False
    if "thanks_sent" in data:
        if data["thanks_sent"] == "on":
            send_thanks = True

    # Try to insert the donor into the db
    donor = None

    # Get donor's name from the POST request
    user_input["first_name"] = data["first_name"]
    user_input["last_name"] = data["last_name"]

    # If the donation was truly anonymous, then the anonymous donor will be returned
    # If the user accidentally left the first and last name blank, then the anonymous donor will be returned
    if ("anonymous" in data and data["anonymous"] == "on") or \
            (user_input["first_name"].strip() == "" and user_input["last_name"].strip() == ""):
        try:
            donor = InsertDonor("ANONYMOUS", "ANONYMOUS", "", "", "", "", "", "", "", "")
        except:
            print("Exception while inserting donor:", end=" ")
            for error in sys.exc_info():
                print(error, end=", ")

    # If the donation was not anonymous, then the database will be queried for the given attributes and that donor will be returned
    else:
        # Set up the rest of the attributes
        user_keys = ["email_address", "phone_number", "state", "city", "zip", "address1", "address2"]
        for key in user_keys:
            if 'anonymous' in data and data['anonymous'] == 'on':
                user_input[key] = "ANONYMOUS"
            else:
                # If the data exists, great. Use it
                if key in data:
                    user_input[key] = data[key].strip()
                # If the data doesn't exist, it stays blank.
                else:
                    user_input[key] = ""

        try:
            # If the donor doesn't exist in the database, then the donor will be created and inserted
            # If they do exist, they will be returned
            donor = InsertDonor(user_input['first_name'], user_input['last_name'],
                                '', user_input['email_address'],
                                user_input['phone_number'],
                                user_input['address1'], user_input['address2'],
                                user_input['city'], user_input['state'],
                                user_input['zip'])
        except:
            print("Exception while inserting donor:", end=" ")
            for error in sys.exc_info():
                print(error, end=", ")

    # Now try to insert the donation. This should fail if donor == None
    # Should technically work even if items_list == []
    try:
        InsertDonation(donor, items_list, data['date_received'], send_thanks, cur_user, data['comment'])
        donation_saved = True
    except:
        print("Exception while inserting donation:", end=" ")
        for error in sys.exc_info():
            print(error, end=", ")
        donation_saved = False

    return donation_saved


def get_donor_list(request):
    if request.method == 'GET':
        list_of_data = list(get_donor_list_wo_anonymous())
        return JsonResponse(list_of_data, safe=False)
    else:
        return HttpResponse("Error")


def view_get_donors(request):
    if request.method == 'GET':

        name_type = bleach.clean(request.GET["name_type"], tags=[], attributes={}, styles=[], protocols=[])
        term = bleach.clean(request.GET["term"], tags=[], attributes={}, styles=[], protocols=[])

        if name_type == "first":
            list_of_data = list(get_donors_w_first_nm(term))
        elif name_type == "last":
            list_of_data = list(get_donors_w_last_nm(term))
        else:
            list_of_data = []
        return JsonResponse(list_of_data, safe=False)
    else:
        return HttpResponse("Error")

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

def edit_businesses(request):
    context = {"form": BusinessEditForm()}
    return render(request, 'input/edit_businesses.html', context)

def get_businesses(request):
    if request.method == 'GET':
        data = Business.objects.values()
        data.order_by("name")
        offset = int(request.GET["offset"])
        limit = int(request.GET["limit"])
        data = data[offset:offset + limit]
        data = list(data)
        json_response = {"rows": data, "total": Business.objects.count()}
        return JsonResponse(json_response, safe=False)
    else:
        return HttpResponse("Error getting businesses")

def add_businesses(request):
    if request.method == "POST":
        form = BusinessForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Business added")
            return redirect('add_businesses')
        else:
            print(f"Error adding business {form.errors}")
            messages.error(request, form.errors)

    return render(request, 'input/add_businesses.html')

def delete_businesses(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            result = Business.objects.filter(name=name).delete()[0]
            if not result:
                return JsonResponse(f"{result}", safe=False)
        except Exception as e:
            print(f"Exception: {e}")
        return HttpResponse("Error")

def update_businesses(request):
    response = {}
    try:
        if request.method != "POST":
            raise Exception("Request not POST")
        update_data = json.loads(request.POST["update_data"])
        print("\"", update_data, "\"",sep="\n")
        filter = {"name": update_data["old_name"]}
        update = {"name": update_data["new_name"]}
        success = update_table_entry(Business, filter, update)
        # business = Business.objects.filter(name=update_data["name"])
        # business.update(update_data["name"])
        # success = business.save()
        if not success:
            raise Exception("Could not change \"" + update_data["old_name"] + "\" to \"" + update_data["new_name"] + "\"")

        response["success"] = True
        response["message"] = business + " successfully added"
        print(response["message"])
    except Exception as e:
        response["success"] = False
        response["message"] = str(e)
        print("Exception:",str(e))
    print("complete")
    return JsonResponse(response, safe=False)
