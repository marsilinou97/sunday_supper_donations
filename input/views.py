from django.shortcuts import render

from .forms import DonarInformationForm


# Create your views here.
def handle_get_req(request):
    form = DonarInformationForm()
    return render(request, 'input/donar-info-form.html', {'form': form})

def handle_post_req(request):
    form = DonarInformationForm(request.POST)
    print(list(request.POST.items()))

    return render(request, 'input/donar-info-form.html')

def index(request):
    if request.method == 'POST':
        return handle_post_req(request)

    form = DonarInformationForm()
    return render(request, 'input/donar-info-form.html', {'form': form})
