# Generated by Django 3.1.6 on 2021-03-31 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0002_auto_20210302_1133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fund',
            options={'ordering': ['item_id']},
        ),
        migrations.AlterField(
            model_name='donation',
            name='comments',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]