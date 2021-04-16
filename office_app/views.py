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


def OfficerRoleCheck(user):    
    return user.is_authenticated and user.role == models.Client.OFFICE_SECRETARY

@user_passes_test(OfficerRoleCheck)
@login_required()
def home(request):
    office = request.user.office
    events = office.RelevantEvents()
    form = forms.EventForm(instance=models.Event(office=office), auto_id=False)

    context = {
        'term': main_models.CurrentTerm,
        'events': events,
        'user': request.user,
        'form': form,
        'clearances': models.Clearance.objects.filter(office=request.user.office,term=main_models.CurrentTerm()),
    }
    return render(request,'offices/home.html',context)

def profile(request):
    return render(request,'offices/profile.html')


@user_passes_test(OfficerRoleCheck)
@login_required()
def event_view(request):
    office = request.user.office
    events = office.RelevantEvents()

    form = forms.EventForm(instance=models.Event(office=office), auto_id=False)

    # office = models.Office.objects.get(secretary=request.user)
    # events = models.Event.objects.filter(office=office) 
    context = {
        'terms':main_models.Term.objects.all(),
        'term': main_models.CurrentTerm(),
        'events':events,
        'user': request.user,
        'form':form
    }
    
    return render(request,'offices/events/event.html',context)



@user_passes_test(OfficerRoleCheck)
@login_required()
def create_event(request):
    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if form.is_valid():
            event = models.Event()
            event.term = main_models.CurrentTerm()
            event.name = form.cleaned_data['name']
            event.office = request.user.office
            event.location = form.cleaned_data['location']
            event.event_datetime_from = form.cleaned_data['event_datetime_from']
            event.event_datetime_to = form.cleaned_data['event_datetime_to']
            event.description = form.cleaned_data['description']
            event.alternative_activity = form.cleaned_data['alternative_activity']
            event.save()
            event.attendees.set(form.cleaned_data['attendees']) 
    
    return redirect('/office/events/')




@user_passes_test(OfficerRoleCheck)
@login_required()
def detail(request, pk):
    event = models.Event.objects.get(pk=pk)    
    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if request.POST['send'] == 'edit':
            if form.is_valid():
                event.term = main_models.CurrentTerm()
                event.name = form.cleaned_data['name']
                event.office = models.Office.objects.get(secretary=request.user) #form.cleaned_data['office']
                event.location = form.cleaned_data['location']
                event.event_datetime_from = form.cleaned_data['event_datetime_from']
                event.event_datetime_to = form.cleaned_data['event_datetime_to']
                event.description = form.cleaned_data['description']
                event.alternative_activity = form.cleaned_data['alternative_activity']
                event.attendees.set(form.cleaned_data['attendees']) 
                event.save()
                return redirect('/office/events/')
        elif request.POST['send'] == 'delete':
            event.delete()
            return redirect('/office/events/')
    else:
        form = forms.EventForm(instance=event, auto_id=False)
    
    context = {
        'term': main_models.CurrentTerm(),
        'event':event,
        'event_id':event.id,
        'form': form.as_p(),
        'user': request.user,
        
    }
    
    return render(request,'offices/events/detail.html',context)
    

@user_passes_test(OfficerRoleCheck)
@login_required()
def delete(request, pk):
    event = models.Event.objects.get(pk=pk)
    event.delete()

    context = {
        'term': main_models.CurrentTerm(),
        'event': event,
        'user': request.user,
        'message': 'Event Successfully Deleted.',
    }

    return render(request,'offices/events/event.html',context)
    
@user_passes_test(OfficerRoleCheck)
@login_required()
def Scan(request):
    splated = request.POST['message'].split('_')
    event = models.Event.objects.get(pk=int(request.POST['event_id']))
    # user = main_models.Client.objects.get(email=request.POST['user_email'])
    timespan = (datetime.datetime.now() - datetime.datetime.strptime(splated[1], "%Y-%m-%d %H:%M:%S"))
    if timespan.total_seconds() <= 17 and event.is_active:
        attendance = models.Attendance()
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



@user_passes_test(OfficerRoleCheck)
@login_required()
def clearances(request):
    context = {
        'term': main_models.CurrentTerm(),
        'terms': main_models.Term.objects.all(),
        'user': request.user,
    }

    return render(request,'offices/clearances/clearances.html',context)



@user_passes_test(OfficerRoleCheck)
@login_required()
def approve_clearance(request, pk):
    clearance = models.Clearance.objects.get(pk=pk)
    clearance.signed = True
    clearance.save()
    return redirect('/office/clearances')


@user_passes_test(OfficerRoleCheck)
@login_required()
def reject_clearance(request, pk):
    if request.method == 'GET':
        clearance = models.Clearance.objects.get(pk=pk)
        clearance.reject_reason = request.GET['reject_reason']
        clearance.signed = False
        clearance.save()
    return redirect('/office/clearances')


@user_passes_test(OfficerRoleCheck)
@login_required()
def cancel_clearance_approval(request, pk):
    clearance = models.Clearance.objects.get(pk=pk)
    clearance.reject_reason = ''
    clearance.signed = False
    clearance.save()
    return redirect('/office/clearances')