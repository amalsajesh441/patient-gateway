from django.contrib import admin
from .models import PatientRecord, AccessLog

admin.site.register(PatientRecord)
admin.site.register(AccessLog)

