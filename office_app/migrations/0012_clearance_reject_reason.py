# Generated by Django 3.1.7 on 2021-04-06 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office_app', '0011_office_is_misc'),
    ]

    operations = [
        migrations.AddField(
            model_name='clearance',
            name='reject_reason',
            field=models.CharField(max_length=255, null=True),
        ),
    ]