from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import PatientRecord, AccessLog
from .serializers import PatientIntakeSerializer
from .utils.fhir import extract_patient_data
from .utils.encryption import encrypt_value, decrypt_value
from .utils.masking import mask_ssn
from .tasks import send_welcome_email

class PatientIntakeView(APIView):
    def post(self, request):
        """
        This endpoint accepts a FHIR R4 Patient JSON payload, validates the data,
        enforces business rules (patient must be 18+), encrypts PHI fields such as
        SSN and Passport, stores the full raw payload for audit purposes, and
        triggers an asynchronous welcome email.
        """
        serializer = PatientIntakeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        fhir_payload = serializer.validated_data["fhir_payload"]

        try:
            patient_data = extract_patient_data(fhir_payload)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        patient = PatientRecord.objects.create(
            patient_id=patient_data["patient_id"],
            full_name=patient_data["full_name"],
            gender=patient_data["gender"],
            birth_date=patient_data["birth_date"],
            encrypted_ssn=encrypt_value(patient_data["ssn"]),
            encrypted_passport=encrypt_value(patient_data["passport"]),
            raw_fhir_payload=fhir_payload,
        )

        send_welcome_email.delay(patient.full_name)

        return Response(
            {"message": "Patient intaked successfully", "id": patient.patient_id},
            status=status.HTTP_201_CREATED,
        )


class PatientRetrieveView(APIView):
    def get(self, request, patient_id):
        """
        This endpoint fetches a stored patient record, decrypts and masks
        sensitive PHI fields (SSN), and logs the access for HIPAA audit
        compliance.
        """
        patient = get_object_or_404(PatientRecord, patient_id=patient_id)

        ssn = decrypt_value(patient.encrypted_ssn)
        masked = mask_ssn(ssn)

        # Audit Log
        AccessLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get("REMOTE_ADDR"),
            patient=patient,
        )

        return Response({
            "patient_id": patient.patient_id,
            "full_name": patient.full_name,
            "gender": patient.gender,
            "birth_date": patient.birth_date,
            "masked_ssn": masked,
        })
