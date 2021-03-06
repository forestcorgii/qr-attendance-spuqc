from django import template
from office_app import models as office_models
from django.db.models.query import EmptyQuerySet
from django.utils import timezone


register = template.Library()

@register.simple_tag
def get_student_attendance(office, student):
    return student.RelevantEvents().filter(office=office)
    
@register.simple_tag
def get_student_absences(office, student, term):
    events = student.RelevantEvents().filter(office=office, term=term)
    absences = [    
        event for event in events
        if not event.attendance_set.filter(student=student).exists()
    ]   
    return absences
    

@register.simple_tag
def get_clearances(term, office):
    return office_models.Clearance.objects.filter(term=term, office=office)    


@register.simple_tag
def get_events(term, office):
    return office_models.Event.objects.filter(term=term, office=office)    


@register.simple_tag
def get_event_today(term, office):
    events = office_models.Event.objects.filter(event_datetime_from=timezone.now())    
    if events.count() > 0:
        return event[0]
    return None 


