from django.db import models
from django.contrib.auth.models import User

class PatientRecord(models.Model):
    patient_id = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    birth_date = models.DateField()

    encrypted_ssn = models.TextField(null=True, blank=True)
    encrypted_passport = models.TextField(null=True, blank=True)

    raw_fhir_payload = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_id


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
