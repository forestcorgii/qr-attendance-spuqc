from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import login,authenticate

from . import models

from . import forms

from student_app import models as student_models

import csv
import io


# Create your views here.
def index(request):    
    if request.user.is_authenticated:    
        return redirect('/accounts/profile/')
    else:
        return redirect('/accounts/login/')


def profile(request):
    if request.user.role == models.Client.STUDENT:
        return redirect('/student/')
    elif request.user.role == models.Client.OFFICE_SECRETARY:
        return redirect('/office/')
    elif request.user.is_admin:
        return redirect('/admin/import/')
        
def admin(request):
    if request.method == 'POST':
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
           file = request.FILES['docfile']
           filetxt = file.read().decode('utf-8')
           io_string = io.StringIO(filetxt)
           for line in csv.reader(io_string, delimiter=',', quotechar='|'):
                client = main_models.Client
                client.role = main_models.Client.STUDENT
                client.id_number = line[0]
                client.email = line[1]
                client.last_name = line[2]
                client.first_name = line[3]
                client.middle_initial = line[4]
                client.password = 'temp1234'
                client.save()

                student = student_models.Student
                student.user = client
                student.course = main_models.Course.objects.get(acronym=line[5])
                student.save()
    else:
        form = forms.DocumentForm()

    context = {
        'user': request.user,
        'form': form,
        'has_permission':True

    }
    # return render('admin/home.html',context)
    return render(request,'admin/home.html',context)



def user_logout(request):
    logout_then_login(request,login_url='/')
    return redirect('/')

def user_login(request):
    auth_failed = False  
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user != None:
            login(request,user)
            return redirect('/')
        else:
            auth_failed = True        
    elif request.method == 'GET' and request.user.is_authenticated:
        return redirect('/')
    else:
        form = forms.LoginForm()
    
    return render(request, 'registration/login.html', {'form': form,'auth_failed':auth_failed})


def import_user(request):
    msg = ''
    if request.method == 'POST':
        form = forms.DocumentForm(request.POST, request.FILES)
        csv_file = request.FILES['docfile']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=',', quotechar='|'):
            user, created = models.Client.objects.get_or_create(email=line[1])           
            if created:
                user.set_password('1234')
            user.id_number = line[0]
            user.role = models.Client.STUDENT
            user.last_name = line[2]
            user.first_name = line[3]
            user.middle_initial = line[4]
            user.save()

            student, created = student_models.Student.objects.get_or_create(user=user)
            student.course = student_models.Course.objects.get(acronym=line[5]) 
            student.save()

            msg = msg + user.email + "\n"
    else:
        form = forms.DocumentForm()
    
    context = {
        'user': request.user,
        'form': form,
        'has_permission':True,
        'msg': msg,        
        }

    return render(request,'admin/import.html',context)
