from django.db import models
from qr_attendance_app.models import Client,Course
from office_app.models import Event
# Create your models here.

class Student(models.Model):
    # student_id = models.IntegerField(primary_key=True,blank=False)
    user = models.OneToOneField(Client, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    

class Attendance(models.Model):
    event = models.ForeignKey(Event,
                                   on_delete=models.CASCADE,
                                   null=True)
    student = models.ForeignKey(Student,
                                   on_delete=models.CASCADE,
                                   null=True)                                   
    datetime_arrived = models.DateTimeField(auto_now_add=True)

    def datetime_arrived_str(self):
        return self.datetime_arrived.strftime("%x %I:%M%p")
    
    def __str__(self):
        return self.id
