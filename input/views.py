from django.shortcuts import render

from .forms import DonationForm, DonorInformationForm, FundsForm, ItemForm


# Create your views here.
def handle_get_req(request):
    form = DonorInformationForm()
    return render(request, 'input/donar-info-form.html', {'form': form})

def handle_post_req(request):
    form = DonorInformationForm(request.POST)
    print(list(request.POST.items()))

    return render(request, 'input/donar-info-form.html')

def index(request):
    if request.method == 'POST':
        return handle_post_req(request)

    return render(request, 'input/donar-info-form.html', 
    {
        'donar_form': DonorInformationForm(), 
        'donation_info_form' : DonationForm(),
        'funds_form': FundsForm(),
        'item_form': ItemForm()
    })
