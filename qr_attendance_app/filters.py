import django_filters
from student_app import models as student_models 

class StudentFilter(django_filters.FilterSet):
    # id = django_filters.CharFilter(field_name='user__id_number',lookup_expr=['exact','contains'])
    class Meta:
        model = student_models.Student
        fields = {'user__id_number':['contains']}
        
