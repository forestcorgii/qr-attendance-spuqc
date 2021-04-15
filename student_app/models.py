from django.db import models
from qr_attendance_app.models import Client, Course, CurrentTerm

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return f"{self.user.id_number} - {self.user.fullname()}"


# @receiver(post_save, sender=Student)
# def student_handler(sender, created, **kwargs):
#     send_mail(
#     'Subject here',
#     """
    
#     """,
#     'seanivanf@gmail.com',
#     ['seanivanf@gmail.com'],
#     )

