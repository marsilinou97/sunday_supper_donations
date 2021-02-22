from django.apps import AppConfig
from django.contrib import admin

from .models import RegistrationToken


class UsersConfig(AppConfig):
    name = 'users'


admin.site.register(RegistrationToken)
