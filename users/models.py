# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User._meta.get_field('email')._unique = True


class RegistrationToken(models.Model):
    token = models.CharField(max_length=128)
    date_created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    expiration_period = models.SmallIntegerField(default=5, validators=[MaxValueValidator(20), MinValueValidator(1)])

    def __str__(self):
        return "Token: {}".format(self.token)
