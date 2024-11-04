# analyzer/admin.py

from django.contrib import admin
from .models import JobApplication

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job_position', 'status', 'date_applied')
    search_fields = ('name', 'email', 'job_position')
    list_filter = ('status', 'date_applied')
    ordering = ('-date_applied',)
    date_hierarchy = 'date_applied'

admin.site.register(JobApplication, JobApplicationAdmin)
