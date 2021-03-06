# Generated by Django 3.1.7 on 2021-03-04 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_attendance_app', '0003_auto_20210305_0024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'permissions': (('office_secretary', 'Office Secretary'), ('student', 'Student'))},
        ),
        migrations.AddField(
            model_name='client',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[('S', 'STUDENT'), ('O', 'OFFICE SECRETARY'), ('H', 'HEAD')], null=True),
        ),
    ]
