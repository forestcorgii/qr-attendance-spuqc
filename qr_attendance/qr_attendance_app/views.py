from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import login,authenticate

from . import models

from . import forms

# Create your views here.
def index(request):    
    if request.user.is_authenticated:    
        return redirect('accounts/profile/')
    else:
        return redirect('accounts/login/')


def profile(request):
    if request.user.role == models.Client.STUDENT:
        return redirect('/student/')
    elif request.user.role == models.Client.OFFICE_SECRETARY:
        return redirect('/office/')
    elif request.user.is_admin:
        return redirect('/admin/other')
        
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
        'form':form
    }
    return render('admin/home.html',context)



def user_logout(request):
    logout_then_login(request,login_url='/')
    return redirect('/')

def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if form.is_valid:
            login(request,user)
            return redirect('/')        
    elif request.method == 'GET' and request.user.is_authenticated:
        return redirect('/')
    else:
        form = forms.LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})
