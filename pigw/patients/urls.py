from django.urls import path
from .views import PatientIntakeView, PatientRetrieveView

urlpatterns = [
    path("api/v1/patient-intake/", PatientIntakeView.as_view()),
    path("api/v1/patients/<str:patient_id>/", PatientRetrieveView.as_view()),
]
