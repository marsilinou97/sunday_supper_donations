# Generated by Django 3.1.6 on 2021-03-03 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationtoken',
            name='expiration_period',
            field=models.SmallIntegerField(default=5),
        ),
    ]
