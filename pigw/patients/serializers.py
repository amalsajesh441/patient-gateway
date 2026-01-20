from rest_framework import serializers
from .models import PatientRecord

class PatientIntakeSerializer(serializers.Serializer):
    fhir_payload = serializers.JSONField()

class PatientResponseSerializer(serializers.ModelSerializer):
    masked_ssn = serializers.CharField()

    class Meta:
        model = PatientRecord
        fields = [
            "patient_id",
            "full_name",
            "gender",
            "birth_date",
            "masked_ssn",
            "created_at",
        ]
