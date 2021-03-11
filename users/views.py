import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from helpers import remove_html_tags
from .forms import UserRegisterForm, RegistrationTokenForm
from .helpers import validate_token

TOKEN_OPTIONS = string.ascii_uppercase + string.ascii_lowercase + string.digits


def handle_post_req(request):
    form = UserRegisterForm(request.POST)

    if form.is_valid():

        token = remove_html_tags(form.cleaned_data.get('token', ''))

        token_error_msg = validate_token(token)
        if token_error_msg:
            messages.error(request, f"Please make sure registration token is valid, {token_error_msg}")
            print("Please make sure registration token is valid")

        else:
            """
            Handle case where email address already exists.
            TODO: This try/except block has a similar purpose with the else statement
            later on, but it's needed to prevent the page from crashing when the
            user tries to register with an email address that already exists in the db
            """
            try:
                form.save()
            except IntegrityError as e:
                print(e)

                # TODO: implement more consistent error messages
                if 'email' in str(e):
                    messages.error(request,f"An account with the email address {request.POST['email']} already exists.")
                else:
                    messages.error(request, f"Please make sure all fields are correct {form.errors}")
                return redirect('register')

            # If an IntegrityError wasn't thrown, account creation was a huge success
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            print(f'Account created for {username}!')

    else:
        form_errors = form.errors
        if "password2" in form_errors:
            form_errors["password"] = form_errors.pop("password2")
        messages.error(request, f"Please make sure all fields are correct {form.errors}")
        print("Form is invalid")

    return redirect('register')


def handle_get_req(request):
    form = UserRegisterForm(initial={'token': request.GET.get('token', '')})
    return render(request, 'users/register.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        # Logged in user can't register
        return redirect("news")
    if request.method == 'POST':
        return handle_post_req(request)
    elif request.method == 'GET':
        return handle_get_req(request)
    else:
        return HttpResponse("What???")


@login_required
def registration_token(request):
    if request.method == 'POST':
        token = ''.join(random.choices(TOKEN_OPTIONS, k=20))
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
        else:
            messages.error(request, f"Please make sure registration token is valid, {form.errors}")
            return render(request, 'users/create_token.html')
    elif request.method == 'GET':
        return render(request, 'users/create_token.html', {'form': RegistrationTokenForm()})
    else:
        HttpResponse("ERROR...")
