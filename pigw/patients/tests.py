from django.test import TestCase
from rest_framework.test import APIClient
from .models import PatientRecord

class PatientAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_patient_intake(self):
        payload = {
            "fhir_payload": {
                "resourceType": "Patient",
                "id": "test-1",
                "name": [{"given": ["John"], "family": "Doe"}],
                "birthDate": "1980-01-01",
                "identifier": [{"system": "http://hl7.org/fhir/sid/us-ssn", "value": "111-22-3333"}]
            }
        }

        response = self.client.post("/api/v1/patient-intake/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(PatientRecord.objects.exists())
