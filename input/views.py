from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from . import models
from .forms import DonationForm, DonorInformationForm, FundsForm, ItemForm, Donor
from django.forms import formset_factory
from django.contrib import messages

from .models import InsertDonor, InsertDonation, InsertItem

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
    user_input = {}

    cur_user = User.objects.last()

    """
    if request.user.is_authenticated:  # authenticates the current user and can't be none
        cur_user = request.User.username
    """

    for a in request.POST:  # loops the input and populates the dictionary
        user_input[a] = request.POST[a]

    print(user_input)

    new_donor = DonorInformationForm(request.POST)
    new_donor.save()

    number_items = user_input['form-TOTAL_FORMS']
    items_list = []  # list of dictionary

    for i in number_items:
        item_dic = {}
        for a in user_input:
            item_dic['subclass'] = user_input['id_form-' + a + '-type']
            item_dic['quantity'] = user_input['id_form-' + a + '-quantity']
            if 'id_form-' + a + '-sub_type_business' in user_input:
                item_dic['businessName'] = user_input['id_form-' + a + '-sub_type_business']
            elif 'id_form-' + a + '-sub_type_clothing' in user_input:
                item_dic['clothingTypeName'] = user_input['id_form-' + a + '-sub_type_clothing']
            elif 'id_form-' + a + '-sub_type_name' in user_input:
                item_dic['name'] = user_input['id_form-' + a + '-sub_type_name']
        items_list.append(item_dic)

    # This one is for funds
    items_list.append({
        
    })

    
    print(items_list)

    """
    InsertDonation(new_donor, items_list, user_input['date_received'], user_input['thanks_sent'], cur_user,
                   user_input['comment'])
    """

    return redirect('input_page')



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
