from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.db import transaction

from settings.queries import *
import settings.queries as queries
import traceback

@login_required
def change_password(request):
    if request.method == 'POST':
        # print(request.POST + '\n\n\n\n')
        form = PasswordChangeForm(request.user, request.POST)
        # print(form)
        # return render(request, "settings/change_password.html")

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password changed')
            return redirect('change_password')
        else:
            print(f"Error updating password {form.error_messages}")
            messages.error(request, form.errors)

    return render(request, "settings/change_password.html")


@login_required
def manage_roles(request):
    if request.user.is_authenticated:
        return render(request, "settings/manage_roles.html")


@login_required
def manage_registration_links(request):
    if request.user.is_authenticated:
        return render(request, "settings/manage_registration_links.html")


@login_required
def manage_registration_links_get_table(request):
    if request.user.is_authenticated:
        return render(request, "settings/manage_registration_links.html")


@login_required
def help(request):
    if request.user.is_authenticated:
        return render(request, "settings/help.html")


@login_required
def index(request):
    if request.method == 'POST':
        return change_password(request)
    """
    if request.user.is_authenticated:
        return render(request,"settings/settings.html")
    """

def get_donor_data(request):
    return JsonResponse(list(get_users_info()), safe=False)

def get_roles(request):
    results = list(get_all_roles())
    flattend_results = list(map(lambda x: x['role'], results))
    return JsonResponse(flattend_results, safe=False)

def update_user_role(request):
    response = {}

    try:
        username = "brad"
        role = "test_group1"
        response.update({"user": username})
        response.update({"role": role})
        with transaction.atomic():
            queries.update_user_role(username, role)
            response.update({"sucess": True})
            response.update({"message": username + " enrolled in " + role})
        return JsonResponse(response)
    except Exception as e:
        response.update({"sucess": False})
        response.update({"message": str(e)})
        return JsonResponse(response)