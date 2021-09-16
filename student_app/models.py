from django.db import models
from qr_attendance_app.models import Client, Course, CurrentTerm, Term

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from qr_attendance_app.templatetags.finance_extras import get_unsigned_clearance

class Student(models.Model):
    # student_id = models.IntegerField(primary_key=True,blank=False)
    user = models.OneToOneField(Client, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)


    def RelevantEvents(self):
        return CurrentTerm().event_set.filter(attendees__pk=self.course.id)

    def RelevantAttendances(self):
        return self.attendance_set.filter(event__term=CurrentTerm())
    
    def RelevantClearances(self):
        return self.clearance_set.filter(term=CurrentTerm())

    def is_completed(self):
        clearances = get_unsigned_clearance(self)
        return len(clearances) == 0

    def __str__(self):
        return self.user.fullname()


class Signature(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	term = models.ForeignKey(Term, on_delete=models.CASCADE)
	verified = models.BooleanField(default=False)
    
# @receiver(post_save, sender=Student)
# def student_handler(sender, created, **kwargs):
#     send_mail(
#     'Subject here',
#     """
    
#     """,
#     'seanivanf@gmail.com',
#     ['seanivanf@gmail.com'],
#     )

