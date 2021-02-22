from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UserRegisterForm
from .helpers import token_exists


def handle_post_req(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        token = form.cleaned_data.get('token', '')
        if not token or not token_exists(token):
            messages.error(request, "Please make sure registration token is valid")
            print("Please make sure registration token is valid")
        else:
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            print(f'Account created for {username}!')
    else:
        messages.error(request, "Please make sure all fields are correct")
        print("Form is invalid")

    return redirect('register')


def handle_get_req(request):
    # form = UserRegisterForm()
    form = UserRegisterForm(initial={'token': request.GET.get('token', '')})
    return render(request, 'users/register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        return handle_post_req(request)
    elif request.method == 'GET':
        return handle_get_req(request)
    else:
        return HttpResponse("What???")
