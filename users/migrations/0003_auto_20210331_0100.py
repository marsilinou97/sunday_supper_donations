# Generated by Django 3.1.6 on 2021-03-31 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210303_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationtoken',
            name='expiration_period',
            field=models.SmallIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)]),
        ),
    ]