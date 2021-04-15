from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from . import models

from django.contrib.auth.decorators import login_required, user_passes_test

import datetime
import io
import segno

from office_app import models as office_models
from office_app import models as main_models

def StudentRoleCheck(user):    
    return user.is_authenticated and user.role == models.Client.STUDENT

@user_passes_test(StudentRoleCheck)
@login_required()
def index(request):
    student = request.user.student
    events = office_models.Event.objects.filter(attendees__pk=student.course.id)
    context = {
        'term': main_models.CurrentTerm(),
        'user': request.user,
        'offices':office_models.Office.objects.all(),
        'events': student.RelevantEvents(),
        'attendances': student.RelevantAttendances(),
    }
    
    return render(request,'student/home.html',context)
    
@user_passes_test(StudentRoleCheck)
@login_required()
def clearances(request):
    student = request.user.student
    
    context = {
        'terms':main_models.Term.objects.all(),
        'term': main_models.CurrentTerm(),
        'offices':office_models.Office.objects.all(),
        'user': request.user,
    }

    return render(request,'student/clearances.html',context)


@user_passes_test(StudentRoleCheck)
@login_required()
def qr_generator(request):
    student = models.Student.objects.get(user=request.user)

    out = io.BytesIO()
    qr = segno.make(("%s_%s") % (student.user.id_number, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    return render(request, 'student/qr-generator.html', {'qr': qr.png_data_uri(scale=10)})
    

@user_passes_test(StudentRoleCheck)
@login_required()
def request_clearance(request, pk):
    office = office_models.Office.objects.get(pk=pk)
    clearance, created = office_models.Clearance.objects.get_or_create(term=main_models.CurrentTerm(), office=office, student=request.user.student)
    if not created:
        clearance.reject_reason = ''
        clearance.signed = False
        clearance.save()

    return redirect('/student/clearances/')

