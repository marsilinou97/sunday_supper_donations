from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def change_password(request):
    if request.method == 'POST':
        print(request.POST + '\n\n\n\n')
        form = PasswordChangeForm(request.user, request.POST)
        print(form)
    return render(request, "settings/change_password.html")
    """
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password changed')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    """


    # return render(request, "settings/change_password.html", {'form': form})

@login_required
def manage_roles(request):
    if request.user.is_authenticated:
        return render(request,"settings/manage_roles.html")

@login_required
def manage_registration_links(request):
    if request.user.is_authenticated:
        return render(request,"settings/manage_registration_links.html")

@login_required
def manage_registration_links_get_table(request):
    if request.user.is_authenticated:
        return render(request,"settings/manage_registration_links.html")

@login_required
def help(request):
    if request.user.is_authenticated:
        return render(request,"settings/help.html")

@login_required
def index(request):
    if request.method == 'POST':
        return change_password(request)
    """
    if request.user.is_authenticated:
        return render(request,"settings/settings.html")
    """