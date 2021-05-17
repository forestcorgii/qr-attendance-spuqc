from django.contrib import admin
from . import models




class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'office', 'event_datetime_from', 'event_datetime_to', 'term')
    
    ordering = ('term',)
    list_filter = ('office','term')
    

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'datetime_arrived')
    # fieldsets = (
    #     (None, {'fields': ('employee_id',)}),
    #     ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name')}),
    #     ('Company Information', {'fields': ('company', 'department', 'project', 'schedule', 'active', 'admin')}),
    # )

    search_fields = ('student__user__id_number','student__user__first_name','student__user__last_name', 'event__name')
    ordering = ('student',)
    list_filter = ('event',)
    

class ClearanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'office', 'signed', 'term')
    
    search_fields = ('student', 'office')
    ordering = ('student',)
    list_filter = ('signed', 'term', 'office')
    

class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'secretary', 'is_misc')
    
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('is_misc', )
    

# Register your models here.
admin.site.register(models.Attendance, AttendanceAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Office, OfficeAdmin)
admin.site.register(models.Clearance, ClearanceAdmin)
