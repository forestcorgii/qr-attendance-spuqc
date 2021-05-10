from django.contrib import admin
from . import models
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    
    ordering = ('user',)
    list_filter = ('course',)
    

admin.site.register(models.Student, StudentAdmin)