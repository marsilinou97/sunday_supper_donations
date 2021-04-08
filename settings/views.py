from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request,"settings/settings.html")

@login_required
def change_password(request):
    if request.user.is_authenticated:
        return render(request,"settings/change_password.html")

@login_required
def manage_roles(request):
    if request.user.is_authenticated:
        return render(request,"settings/manage_roles.html")

@login_required
def manage_registration_links(request):
    if request.user.is_authenticated:
        return render(request,"settings/manage_registration_links.html")

@login_required
def help(request):
    if request.user.is_authenticated:
        return render(request,"settings/help.html")
