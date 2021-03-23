from django.db import models
from qr_attendance_app.models import Client,Course,Location
# Create your models here.

import datetime

class Office(models.Model):
    office_name = models.CharField(max_length=75)
    secretary = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    Head = models.CharField(max_length=75, null=True)
    
    def __str__(self):
        return self.office_name


class Event(models.Model):    
    name = models.CharField(max_length=75)
    office = models.ForeignKey(Office,
                                   on_delete=models.CASCADE,
                                   null=True)

    event_datetime_from = models.DateTimeField(blank=False, null=True)
    event_datetime_to = models.DateTimeField(blank=False, null=True)

    description = models.TextField(blank=True,null=True)
    attendees = models.ManyToManyField(Course,null=True,blank=False)    

    location = models.ForeignKey(Location,
                                   on_delete=models.CASCADE,
                                   null=True)

    alternative_activity = models.TextField(blank=True,null=True)



    def validate_event_datetime(self):
        return (event_datetime_to - event_datetime_from).total_seconds > 0

    def is_active(self):
        timespan = datetime.datetime.now() - self.event_datetime_from 
        return timespan.total_seconds > -(15 * 60) and timespan.total_seconds < (15 * 60)

    def event_date_str(self):
        return self.event_datetime_from.strftime("%m/%d/%Y")


    def event_datetime_from_str(self):
        return self.event_datetime_from.strftime("%m/%d/%Y %I:%M%p")

    def event_datetime_to_str(self):
        return self.event_datetime_to.strftime("%m/%d/%Y %I:%M%p")
    

    def event_time_to_str(self):
        return self.event_datetime_to.strftime("%I:%M%p")

    def event_time_from_str(self):
        return self.event_datetime_from.strftime("%I:%M%p")

    def event_day_str(self):
        return self.event_datetime_from.strftime("%d")
    
    def event_day_word_str(self):
        return self.event_datetime_from.strftime("%A")
    
    def event_month_str(self):
        return self.event_datetime_from.strftime("%b")
    