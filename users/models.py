# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class RegistrationToken(models.Model):
    token = models.CharField(max_length=128)
    date_created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    expiration_period = models.SmallIntegerField(default=7)

    def __str__(self):
        return "Token: {}".format(self.token)
