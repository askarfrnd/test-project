from django.contrib import admin
from .models import LogDetail


class LogDetailAdmin(admin.ModelAdmin):
    list_display = ['email', 'timestamp_created', 'trial_no_email', 'status_email', 'type']
    list_filter = ['timestamp_created', 'status_email']


admin.site.register(LogDetail)
