from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

from . import models

from django.contrib.auth.decorators import login_required,user_passes_test

import datetime
import io
import segno

from office_app import models as officeModels

def StudentRoleCheck(user):    
    return user.is_authenticated and user.role == models.Client.STUDENT

@user_passes_test(StudentRoleCheck)
@login_required()
def index(request):
    student = request.user.student
    events = officeModels.Event.objects.filter(attendees__pk=student.course.id)
    context = {
        'user': request.user,
        'events': events
    }
    
    return render(request,'student/home.html',context)
    
@user_passes_test(StudentRoleCheck)
@login_required()
def clearances(request):
    student = request.user.student
    
    context = {
        'user': request.user,
    }

    return render(request,'student/clearances.html',context)


@user_passes_test(StudentRoleCheck)
@login_required()
def qr_generator(request):
    student = models.Student.objects.all()[0]

    out = io.BytesIO()
    qr = segno.make(("%s_%s") % (student.user.id_number, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    return render(request, 'student/qr-generator.html', {'qr': qr.png_data_uri(scale=10)})
    

