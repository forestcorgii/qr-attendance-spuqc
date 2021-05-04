from django_filters import FilterSet, BooleanFilter
from django_filters.widgets import BooleanWidget


from student_app import models as student_models 
from office_app import models as office_models 

class Student(FilterSet):
    # id = django_filters.CharFilter(field_name='user__id_number',lookup_expr=['exact','contains'])
    class Meta:
        model = student_models.Student
        fields = {'user__id_number':['contains']}
        


class Clearance(FilterSet):
    
    class Meta:
        model = office_models.Clearance
        fields = {'student__user__id_number':['contains'],'term':['exact'],'signed':['exact']}
        
