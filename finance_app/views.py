from django.shortcuts import render

from qr_attendance_app import models as main_models
from office_app import models as office_models
from student_app import models as student_models
from qr_attendance_app import filters

from django.core.mail import send_mail

def home(request):

    # completed = request.GET.get('completed',None)
    # qs = student_models.Student.objects.all()
    # if completed == 'yes':
        
    students = filters.Student(request.GET, queryset=student_models.Student.objects.all())
    
    context = {
        'term': main_models.CurrentTerm,
        'user':request.user,
        'students': students,
    }

    return render(request,"finance/home.html",context)