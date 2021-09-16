from django.shortcuts import redirect, render

from qr_attendance_app import models as main_models
from office_app import models as office_models
from student_app import models as student_models
from qr_attendance_app import filters

from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required,user_passes_test

def home(request):

    id = request.GET.get('id_number', None)
    completed = request.GET.get('completed', None)
    course = request.GET.get('course', None)

    if id == None:
        qs = student_models.Student.objects.all()
    else:
        qs = student_models.Student.objects.filter(user__id_number__contains=id)

    if course != None:
        qs = student_models.Student.objects.filter(course=main_models.Course.objects.filter(acronym=course)[0])

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
        'courses': main_models.Course.objects.all(),
        'filter':{'id_number': id, 'completed': completed, 'course': course}
    }

    return render(request,"finance/home.html",context)

@login_required()
def verify(request):
    student_id = request.POST.get('student_id', None)
    if student_id != None:
        student = student_models.Student.objects.get(user__id_number=student_id)
        if student != None:
            signature = student_models.Signature(student=student, term=main_models.CurrentTerm(), verified=True)
            signature.save()
    return redirect("/")
