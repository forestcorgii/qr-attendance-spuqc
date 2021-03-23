from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader

from django.views.generic import ListView

from django.contrib.auth.decorators import login_required,user_passes_test


from qr_attendance_app import models as main_models
from student_app import models as student_models

from . import models
from . import forms

import datetime

import csv
import io


def OfficerRoleCheck(user):    
    return user.is_authenticated and user.role == models.Client.OFFICE_SECRETARY

@user_passes_test(OfficerRoleCheck)
@login_required()
def home(request):
    current_event = models.Event.objects.filter(event_datetime_from__date=datetime.date.today())
    context = {'current_event': current_event}
    return render(request,'offices/home.html',context)

def profile(request):
    return render(request,'offices/profile.html')


@user_passes_test(OfficerRoleCheck)
@login_required()
def event(request):
    office = models.Office.objects.get(secretary=request.user)
    events = models.Event.objects.filter(office=office) 

    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/office/events/')
    else:
        form = forms.EventForm(instance=models.Event(office=office), auto_id=False)

    # office = models.Office.objects.get(secretary=request.user)
    # events = models.Event.objects.filter(office=office) 
    context = {
        'events':events,
        'office': office,
        'form':form
    }
    
    return render(request,'offices/events/event.html',context)

@user_passes_test(OfficerRoleCheck)
@login_required()
def detail(request, pk):
    event = models.Event.objects.get(pk=pk)    
    # if request.method == 'POST':
    #     form = forms.EventForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/')
    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if request.POST['send'] == 'edit':
            if form.is_valid():
                event.name = form.cleaned_data['name']
                event.office = models.Office.objects.get(secretary=request.user) #form.cleaned_data['office']
                event.event_datetime_from = form.cleaned_data['event_datetime_from']
                event.event_datetime_to = form.cleaned_data['event_datetime_to']
                event.description = form.cleaned_data['description']
                event.attendees.set(form.cleaned_data['attendees']) 
                event.save()
                return redirect('/office/events/')
        elif request.POST['send'] == 'delete':
            event.delete()
            return redirect('/office/events/')
    else:
        form = forms.EventForm(instance=event, auto_id=False)
    
    
    
    context = {
        'event':event,
        'event_id':event.id,
        'form': form.as_p(),
        'user':request.user
    }
    
    return render(request,'offices/events/detail.html',context)
    

@user_passes_test(OfficerRoleCheck)
@login_required()
def delete(request, pk):
    event = models.Event.objects.get(pk=pk)
    event.delete()

    context = {
        'event': event,
        'user': request.user,
        'message': 'Event Successfully Deleted.',
    }

    return render(request,'offices/events/event.html',context)
    

def Scan(request):
    splated = request.POST['message'].split('_')
    event = models.Event.objects.get(pk=int(request.POST['event_id']))
    # user = main_models.Client.objects.get(email=request.POST['user_email'])
    timespan = (datetime.datetime.now() - datetime.datetime.strptime(splated[1], "%Y-%m-%d %H:%M:%S"))
    if timespan.total_seconds() <= 17 and event.is_active:
        attendance = student_models.Attendance()
        attendance.event = event
        attendance.student = student_models.Student.objects.get(user__id_number=splated[0])
        attendance.save()
        user = attendance.student.user
        return HttpResponse("""Successfully scanned:
        Student ID: {0}
        Fullname: {1}
        E-mail: {2}
        """.format(user.id_number,user.id_number, user.email))
    return HttpResponse('somthing went wrong, please try again.')

