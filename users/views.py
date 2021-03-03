from django.contrib import messages
from django.db.transaction import commit
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UserRegisterForm, RegistrationTokenForm
from .helpers import token_exists
from django.contrib.auth.decorators import login_required


def handle_post_req(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        token = form.cleaned_data.get('token', '')
        if not token or not token_exists(token):
            messages.error(request, "Please make sure registration token is valid")
        else:
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
    else:
        messages.error(request, "Please make sure all fields are correct")
        print("Form is invalid")

    return redirect('register')


def handle_get_req(request):
    form = UserRegisterForm(initial={'token': request.GET.get('token', '')})
    return render(request, 'users/register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        return handle_post_req(request)
    elif request.method == 'GET':
        return handle_get_req(request)
    else:
        return HttpResponse("What???")


import random, string

token_options = string.ascii_uppercase + string.ascii_lowercase + string.digits
from django.urls import reverse


@login_required
def registration_token(request):
    if request.method == 'POST':
        token = ''.join(random.choices(token_options, k=20))
        form = RegistrationTokenForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.creator = request.user
            form.token = token
            form.save()

            return render(request, 'users/create_token.html',
                          {'token': "%s%s%s" % (
                              request.build_absolute_uri('/')[:-1],
                              reverse('register'),
                              "?token=" + token)
                           })
        return render(request, 'users/create_token.html')
    elif request.method == 'GET':
        return render(request, 'users/create_token.html', {'form': RegistrationTokenForm()})
    else:
        HttpResponse("ERROR...")
