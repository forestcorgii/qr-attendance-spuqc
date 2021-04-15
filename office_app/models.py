from django.db import models
from qr_attendance_app.models import Client, Course, Location, Term, CurrentTerm
from student_app.models import Student
# Create your models here.

from django.utils import timezone
import datetime

from django.core.mail import send_mail

from django.db.models.signals import post_save
from django.dispatch import receiver

class Office(models.Model):
    name = models.CharField(max_length=75)
    secretary = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    Head = models.CharField(max_length=75, null=True)
    
    is_misc = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def RelevantEvents(self):
        return self.event_set.filter(term=CurrentTerm())


class Event(models.Model):
    class Meta:
        ordering = ['-event_datetime_from']

    name = models.CharField(max_length=75)
    term = models.ForeignKey(Term,
                                   on_delete=models.CASCADE,
                                   null=True)
    office = models.ForeignKey(Office,
                                   on_delete=models.CASCADE,
                                   null=True)

    event_datetime_from = models.DateTimeField(blank=False, null=True)
    event_datetime_to = models.DateTimeField(blank=False, null=True)

    description = models.TextField(blank=True,null=True)
    attendees = models.ManyToManyField(Course)    

    location = models.ForeignKey(Location,
                                   on_delete=models.CASCADE,
                                   null=True)

    alternative_activity = models.TextField(blank=True,null=True)



    def validate_event_datetime(self):
        return (self.event_datetime_to - self.event_datetime_from).total_seconds > 0

    @property
    def is_active(self):
        timespan = (timezone.now() - self.event_datetime_from)
        return timespan.total_seconds() > -(15 * 60) and timespan.total_seconds() < (100 * 60)
    
    @property
    def has_opened(self):
        return (timezone.now() - self.event_datetime_from).total_seconds() > -(15 * 60)

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
    
    def __str__(self):
        return self.name



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
        return f"{self.student.user.fullname()} - {self.datetime_arrived_str()}"



class Clearance(models.Model):
    office = models.ForeignKey(Office,
                                   on_delete=models.CASCADE,
                                   null=True)

    student = models.ForeignKey(Student,
                                   on_delete=models.CASCADE,
                                   null=True)

    term = models.ForeignKey(Term,
                                   on_delete=models.CASCADE,
                                   null=True)

    reject_reason = models.CharField(max_length=255, default='', blank=True)

    signed = models.BooleanField(default=False)

    def is_rejected(self):
        return (not reject_reason is None)

    def approve_Clearance(self):
        self.signed = True
        self.save()
    
    def reject_clearance(self, reason):
        self.reject_reason = reason
        self.save()

    def __str__(self):
        return f"{self.office} - {self.student.user.fullname()}"






@receiver(post_save, sender=Event)
def Event_handler(sender, instance, created, **kwargs):
    subject = ''
    content = ''
    sender = 'seanivanf@gmail.com'
    receiver = []
    
    # for course in instance.attendance_set.all():
    #     for student in course.student_set.all():
    #         receiver.append(student.user.email)

    receiver.append('seanivanf@gmail.com')
    # receiver.append('rcdejesus@spuqc.edu.ph')
    # receiver.append('apadua@spuqc.edu.ph')
    receiver.append('seanivanf@yahoo.com')

    if created:
        subject = 'An Event has been posted..'
    else:
        subject = f'{instance.name} has been editted.'


    content = f'''

    Name: {instance.name}
    Date: {instance.event_date_str()}
    From: {instance.event_time_from_str()} To: {instance.event_time_to_str()}
    Description: {instance.description}

    Failure to attend will be required to:
    {instance.alternative_activity}

    '''

    send_mail(
    subject,
    content,
    sender,
    receiver,
    )



@receiver(post_save, sender=Clearance)
def clearance_handler(sender, instance, created, **kwargs):
    subject = ''
    content = ''
    sender = ''
    receiver = []

    if created:        
        # send to office
        sender = 'seanivanf@gmail.com'
        receiver = ['seanivanf@gmail.com']
        
        subject = f'{instance.student.user.fullname()} Clearance'
        content = f'''

        Mr/Ms. {instance.user.fullname()} sent a clearance request.

        '''
    else:
        # send to student
        sender = 'seanivanf@gmail.com'
        receiver = ['seanivanf@gmail.com']

        if instance.signed:            
            subject = f'{instance.office} - Approved Clearance Request'
            content = f'''

            {instance}

            '''
        else:
            subject = f'{instance.office} - Rejected Clearance Request'
            content = f'''

            Your request was rejected due to the following reason/s:
            {instance.reject_reason}

            '''

    send_mail(
    subject,
    content,
    sender,
    receiver,
    )



@receiver(post_save, sender=Attendance)
def attendance_handler(sender, instance, created, **kwargs):
    subject = f"{instance.event} Attendance receipt"
    content = ''
    sender = 'seanivanf@gmail.com'
    receiver = ['seanivanf@gmail.com']

    if created:
        subject = 'Term opened.'
        content = f'''

        Event: {instance.event}
        Attended at: {instance.datetime_arrived_str}

        '''

    send_mail(
    subject,
    content,
    sender,
    receiver,
    )
