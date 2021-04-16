from django import template
from office_app import models as office_models
from django.db.models.query import EmptyQuerySet

register = template.Library()

@register.simple_tag
def get_student_attendance(office, student):
    return student.RelevantEvents().filter(office=office)
    
@register.simple_tag
def get_student_absences(office, student):
    events = student.RelevantEvents().filter(office=office)
    absences = [    
        event for event in events
        if not event.attendance_set.filter(student=student).exists()
    ]   
    return absences
    

@register.simple_tag
def get_clearances(term, office):
    return office_models.Clearance.objects.filter(term=term, office=office)    
