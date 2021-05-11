from django.shortcuts import render

from qr_attendance_app import models as main_models
from office_app import models as office_models
from student_app import models as student_models
from qr_attendance_app import filters

from django.core.mail import send_mail

def home(request):

    id = request.GET.get('id_number', None)
    completed = request.GET.get('completed', None)

    qs = student_models.Student.objects.filter(user__id_number__contains=id)
    if completed == 'true':
        qs = [    
            student for student in qs
            if student.is_completed()
        ]
    elif completed == 'false':
        qs = [    
            student for student in qs
            if not student.is_completed()
        ]
        
    # students = filters.Student(request.GET, queryset=qs)
    
    context = {
        'term': main_models.CurrentTerm,
        'user':request.user,
        'students': qs,
        'filter':{'id_number': id, 'completed': completed}
    }

    return render(request,"finance/home.html",context)