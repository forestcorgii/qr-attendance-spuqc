from django import template

from office_app import models as office_models
from student_app import models as student_models
from qr_attendance_app import models

from django.db.models.query import EmptyQuerySet

register = template.Library()

@register.simple_tag
def get_unsigned_clearance(student):
    offices = office_models.Office.objects.all()
    unsigned_clearances = [    
        office for office in offices
        if not office.clearance_set.filter(student=student, term=models.CurrentTerm(),signed=True).exists()
    ]
    return unsigned_clearances