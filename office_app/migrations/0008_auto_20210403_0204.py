# Generated by Django 3.1.7 on 2021-04-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_attendance_app', '0013_remove_course_is_active'),
        ('office_app', '0007_auto_20210402_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(to='qr_attendance_app.Course'),
        ),
    ]
