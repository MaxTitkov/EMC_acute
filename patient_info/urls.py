from django.urls import path
from .views import AllPAtientsListView, PatientListView, PatientActiveListView, SearchPatient, hide_patient, PatientDetailView, RecordDetailView, PatientCreateView, PatientUpdateView, RecordCreateView, RecordUpdateView

urlpatterns = [
    path("", PatientListView.as_view(), name="PatientList"),
    path("patients-active/", PatientActiveListView.as_view(), name="PatientsActiveList"),
    path("delete-patient_<int:patient_id>", hide_patient, name="DeletePatient"),
    path("<int:pk>/", PatientDetailView.as_view(), name="PatientDetail"),
    path("<int:patient_id>/record/<int:pk>", RecordDetailView.as_view(), name="RecordDetail"),
    path("create_patient", PatientCreateView.as_view(), name="PatientCreate"),
    path("update_patient/<int:pk>", PatientUpdateView.as_view(), name="PatientUpdate"),
    path("create_record/<int:patient_id>", RecordCreateView.as_view(), name="RecordCreate"),
    path("update_record/patient/<int:patient_id>/record/<int:pk>", RecordUpdateView.as_view(), name="RecordUpdate"),
    path('search/', SearchPatient, name="Search"),
    path("all", AllPAtientsListView.as_view(), name="AllPatients"),
]