# Generated by Django 3.1.7 on 2021-03-14 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qr_attendance_app', '0010_remove_client_course'),
        ('office_app', '0002_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qr_attendance_app.course'),
        ),
    ]
