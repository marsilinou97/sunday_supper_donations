from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import JsonResponse
from django.db import transaction, IntegrityError
from django.utils.translation import activate

from settings.forms import *
from settings.queries import *
from users.models import RegistrationToken
import settings.queries as queries
import traceback
import json

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

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
@permission_required('auth.change_user')
def manage_roles(request):
    if request.user.is_authenticated:
        form = UserRoleForm()
        context = {"form": form}
        return render(request, "settings/manage_roles.html", context)

@login_required
@permission_required('users.change_registrationtoken')
def manage_registration_links(request):
    if request.user.is_authenticated:
        form = TokenForm()
        context = {"form": form}
        return render(request, "settings/manage_registration_links.html", context)

@login_required
def help(request):
    if request.user.is_authenticated:
        return render(request, "settings/help.html")

@login_required
def index(request):
    if request.method == 'POST':
        return change_password(request)

@login_required
@permission_required('auth.change_user')
def get_user_data(request):
    if request.method != "GET":
        return HttpResponse("Error")
    offset = int(request.GET["offset"])
    limit = int(request.GET["limit"])
    json_response = {"rows":list(queries.get_users_info(offset, limit))}
    return JsonResponse(json_response, safe=False)
    # return JsonResponse(list(get_users_info()), safe=False)

@login_required
@permission_required('auth.change_user')
def get_roles(request):
    results = list(get_all_roles())
    flattend_results = list(map(lambda x: x['role'], results))
    return JsonResponse(flattend_results, safe=False)

@login_required
@permission_required('auth.change_user')
def update_user_role(request):
    response = {}

    try:
        if request.method != "POST":
            raise Exception("Request not POST")

        id = request.POST['id']
        role = request.POST['role']
        response.update({"user": id})
        response.update({"role": role})

        with transaction.atomic():
            queries.update_user_role(id, role)

        response.update({"success": True})
        response.update({"message": str(id) + " enrolled in " + role})
        return JsonResponse(response)
    except Exception as e:
        response.update({"success": False})
        response.update({"message": str(e)})
        return JsonResponse(response)

@login_required
@permission_required('auth.change_user')
def activate_user(request):
    response = {}

    try:
        if request.method != "POST":
            raise Exception("Request not POST")

        id = request.POST["id"]
        active = request.POST["active"]

        response.update({"id": id})
        response.update({"active": active})

        with transaction.atomic():
            queries.activate_user(id, active)

        response.update({"success": True})
        response.update({"message": str(id) + " | activated: " + str(active)})

        return JsonResponse(response, safe= False)

    except Exception as e:
        response.update({"success": False})
        response.update({"message": str(e)})
        return JsonResponse(response)

@login_required
@permission_required('users.change_registrationtoken')
def get_token_data(request):

    if request.method != "GET":
        return HttpResponse("ERROR...")

    offset = int(request.GET["offset"])
    limit = int(request.GET["limit"])
    rows_count = RegistrationToken.objects.count()
    json_response = {"rows":list(queries.get_token_data(offset, limit)), "total": rows_count}
    return JsonResponse(json_response, safe=False)
    # return JsonResponse(list(queries.get_token_data()), safe=False)

@login_required
@permission_required('users.change_registrationtoken')
def update_token_data(request):

    try:
        if request.method != "POST":
            raise Exception("Request not POST")

        response = {}

        update_data = json.loads(request.POST["update_data"])
        token_id = update_data["id"]

        # creator_name isn't in the users_registrationtoken table
        update_data.pop("creator_name")

        #just to be safe
        if update_data["active"] == "True":
            update_data["active"] = True
        else:
            update_data["active"] = False

        with transaction.atomic():
            success = queries.update_token_data(token_id, update_data)#[0]
            if not success:
                raise Exception("Token id: " + str(token_id) + " not updated")

        response.update({"success": True})
        response.update({"message": "Token id: " + str(token_id) + " updated"})
        return JsonResponse(response, safe= False)

    except Exception as e:
        response.update({"success": False})
        response.update({"message": str(e)})
        return JsonResponse(response, safe=False)

@login_required
@permission_required('users.change_registrationtoken')
def delete_token(request):
    try:
        if request.method != "POST":
            raise Exception("Request not POST")

        response = {}

        print("request.POST",request.POST,sep="\n")
        token_id = request.POST["token_id"]
        print("token id:",token_id)

        with transaction.atomic():
            success = queries.delete_token(token_id)
            if not success:
                raise Exception("Token id: " + str(token_id) + " not deleted")

        response.update({"success": True})
        response.update({"message": "Token id: " + str(token_id) + " deleted"})
        return JsonResponse(response, safe= False)

    except Exception as e:
        response.update({"success": False})
        response.update({"message": str(e)})
        return JsonResponse(response, safe=False)
