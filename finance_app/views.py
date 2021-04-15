from django.shortcuts import render

from qr_attendance_app import models as main_models
from office_app import models as office_models
from student_app import models as student_models
from qr_attendance_app.filters import StudentFilter

from django.core.mail import send_mail

def home(request):
    # for i in range(10):
    #     office_models.Event.objects.all()[0].save()
    
    filter = StudentFilter(request.GET, queryset=student_models.Student.objects.all())
    
    context = {
        'term': main_models.CurrentTerm,
        'user':request.user,
        'students': filter,
    }

    return render(request,"finance/home.html",context)