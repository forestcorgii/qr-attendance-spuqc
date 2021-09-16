# Generated by Django 3.1.7 on 2021-09-16 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qr_attendance_app', '0016_auto_20210412_2318'),
        ('student_app', '0003_delete_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.student')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qr_attendance_app.term')),
            ],
        ),
    ]