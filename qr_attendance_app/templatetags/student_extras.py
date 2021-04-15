from django import template
from office_app import models as office_models
from django.db.models.query import EmptyQuerySet

from qr_attendance_app import models 

register = template.Library()

@register.simple_tag
def has_attended(event, student):
    return event.attendance_set.filter(student=student).count() > 0

@register.simple_tag
def get_clearance(term ,office, student):
    clearance = office_models.Clearance.objects.filter(term=term, office=office, student=student)
    if clearance.count() > 0:
        return clearance[0]
    else:
        return None

    
