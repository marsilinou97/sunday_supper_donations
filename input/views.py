from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import DonationForm, DonorInformationForm, FundsForm, ItemForm, Donor
from django.forms import formset_factory
from django.contrib import messages

from .models import *

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
    cur_user = User.objects.last()  # who is the current user
    user_input_items = {}  # items dictionary
    items_list = []  # list of dictionary for item types

    number_items = 0
    count = 0  # controller

    for a in request.POST:  # loops the input and populates the dictionary
        user_input[a] = request.POST[a]
        count += 1
        user_input['comment'] = "NEEDS WORK"
        if count == 15:  # to get the amount on item in the user input
            number_items = int(user_input['form-TOTAL_FORMS'])
        elif count >= 19:  # if the input is on the items
            user_input_items[a] = request.POST[a]  # put the data on another dictionary

    user_input_fundTypeName = user_input['type']
    user_input_fund_amount = user_input['amount']

    print(user_input)
    print(user_input_items)

    # the fund type and amount, needs to be on the first
    items_list.append({})
    items_list[0]['quantity'] = 1
    items_list[0]['subclass'] = Fund
    items_list[0]['amount'] = user_input_fund_amount
    items_list[0]['fundTypeName'] = user_input_fundTypeName

    # another for loop that will put the user_input_items in the items_list in a dictionary with 3 pairs

    for i in range(0, number_items):
        item_dic = {}
        for a in range(0, len(user_input_items)):
            item_dic['type'] = user_input_items['id_form-' + str(i) + '-type']

            if item_dic['type'] == 'giftcard':
                item_dic['subclass'] = GiftCard
                item_dic['amount'] = -999 # TODO: fix once the form has an amount for Giftcards
            elif item_dic['type'] == 'clothing':
                item_dic["subclass"] = Clothing
            elif item_dic['type'] == 'food':
                item_dic["subclass"] = Food
            elif item_dic['type'] == 'misc':
                item_dic["subclass"] = Miscellaneous

            item_dic['quantity'] = user_input_items['id_form-' + str(i) + '-quantity']

            # Giftcard
            if 'id_form-' + str(i) + '-sub_type_business' in user_input_items:
                item_dic['businessName'] = user_input_items['id_form-' + str(i) + '-sub_type_business']

            # Clothing
            elif 'id_form-' + str(i) + '-sub_type_clothing' in user_input_items:
                item_dic['clothingTypeName'] = user_input_items['id_form-' + str(i) + '-sub_type_clothing']

            # Food/Misc
            elif 'id_form-' + str(i) + '-sub_type_name' in user_input_items:
                item_dic['name'] = user_input_items['id_form-' + str(i) + '-sub_type_name']
        items_list.append(item_dic)
    # for i in range(0,number_items):
    #     temp_item = {}
    #     num_items_in_dic = 0
    #     for a in user_input_items:
    #         temp_item[a] = user_input[a]
    #         num_items_in_dic += 1
    #         if num_items_in_dic == 3:
    #             break
    #     items_list.append(temp_item)

    # for a in items_list:
    #     print(a)
    #     a["key"] = "value"

    if "anonymous" in user_input:
        if user_input['anonymous'] == 'on':
            user_input['first_name'] = 'ANONYMOUS'
            user_input['last_name'] = 'ANONYMOUS'
            user_input['state'] = ' '

    new_donor = InsertDonor(user_input['first_name'], user_input['last_name'], '', user_input['email'],
                            user_input['phone_number'], user_input['address1'], user_input['address2'],
                            user_input['city'], user_input['state'], user_input['zip'])

    print(items_list)
    # InsertDonation(new_donor, items_list, user_input['date_received'], user_input['thanks_sent'], cur_user, "None")
    InsertDonation(new_donor, items_list, user_input['date_received'], True , cur_user, "None")
    return redirect('input_page')

    """
    if request.user.is_authenticated:  # authenticates the current user and can't be none
        cur_user = request.User.username
    """

    """

    # populating items_list with items thats not funds
    """
    """
    for i in range(0,number_items):
        item_dic = {}
        for a in range(0,len(user_input)):
            item_dic['type'] = user_input['id_form-' + str(a) + '-type']
            item_dic['quantity'] = user_input['id_form-' + str(a) + '-quantity']

            # Giftcard
            if 'id_form-' + str(a) + '-sub_type_business' in user_input:
                item_dic['businessName'] = user_input['id_form-' + str(a) + '-sub_type_business']

            # Clothing
            elif 'id_form-' + str(a) + '-sub_type_clothing' in user_input:
                item_dic['clothingTypeName'] = user_input['id_form-' + str(a) + '-sub_type_clothing']

            # Food/Misc
            elif 'id_form-' + str(a) + '-sub_type_name' in user_input:
                item_dic['name'] = user_input['id_form-' + str(a) + '-sub_type_name']
        items_list.append(item_dic)
    """
    # This one is for fund types

    # items_list.append({})





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
