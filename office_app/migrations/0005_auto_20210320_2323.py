# Generated by Django 3.1.7 on 2021-03-20 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_attendance_app', '0010_remove_client_course'),
        ('office_app', '0004_auto_20210319_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(null=True, to='qr_attendance_app.Course'),
        ),
    ]
