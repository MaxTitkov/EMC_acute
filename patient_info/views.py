from django.shortcuts import render, render_to_response
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import Patient, Info
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import AddRecordForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from accounts.models import Profile
from django.contrib.auth.models import User

class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = Patient.objects.filter(hided=False).order_by("-is_active", "fullname",)
    # paginate_by = 20
    context_object_name = "patients"
    template_name="patient_info/patients.html"


    def test_func(self):
        # return self.request.user.email.endswith("@emcmos.ru")
        # profile = Profile.objects.get(user = self.request.user)
        # return profile.occupation == "D"
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.request.user)
        context["profile"] = profile.occupation
        return context


@login_required
def hide_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.hided = True
    patient.save()
    return redirect(reverse_lazy("AllPatients"))

class PatientActiveListView(LoginRequiredMixin, ListView):
    queryset = Patient.objects.filter(is_active=True).order_by("room")
    context_object_name = "patients"
    template_name="patient_info/patients_active.html"

class PatientDetailView(LoginRequiredMixin, DetailView):

    model = Patient
    context_object_name = "patient"
    template_name = "patient_info/patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = Info.objects.filter(patient=self.object)
        return context

class RecordDetailView(LoginRequiredMixin, DetailView):
    model = Info
    context_object_name = "record"
    template_name = "patient_info/record_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.objects.get(id=self.kwargs["patient_id"])
        return context

class PatientCreateView(LoginRequiredMixin, CreateView):
    model=Patient
    context_object_name = "patient"
    fields = ["fullname", "dob", "room", "is_active",]
    template_name = "patient_info/create_patient.html"
    success_url = reverse_lazy('PatientList')


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model=Patient
    context_object_name = "patient"
    fields = ["fullname", "dob", "room", "is_active", "srisk", "drisk", "self_harm"]
    template_name = "patient_info/update_patient.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy("PatientDetail", kwargs={'pk': self.kwargs["pk"]})

class RecordCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AddRecordForm(request.POST)
        form.initial['patient'] = Patient.objects.get(id=self.kwargs["patient_id"])
        # form.initial['owner'] = User.objects.get(username = request.user)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            # bathroom_time = form["bathroom"]
            form.save()
            return redirect(reverse_lazy("PatientDetail", kwargs={"pk": self.kwargs["patient_id"]}))
        return render(request, "patient_info/create_record.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = AddRecordForm()
        form.initial['patient'] = Patient.objects.get(id=self.kwargs["patient_id"])
        patient_id = self.kwargs["patient_id"]
        patient_name = Patient.objects.get(id=self.kwargs["patient_id"]).fullname
        patient = Patient.objects.get(id=self.kwargs["patient_id"])
        return render(request, "patient_info/create_record.html", {"form": form, "patient_id": patient_id, "patient_name": patient_name, "patient": patient})

    
class RecordUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model=Info
    context_object_name = "record"
    fields = ["suicidal_risk", "bathroom_time", "record",]
    template_name = "patient_info/update_record.html"
    success_message = "Запись изменена"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = Patient.objects.get(id=self.kwargs["patient_id"])
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("PatientDetail", kwargs={'pk': self.kwargs["patient_id"]})
    
    # Only owner allow to update
    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.add_message(request, messages.INFO, extra_tags="alert-danger alert-dismissible",message='Вы можете менять только свои записи')
            return redirect(reverse_lazy("PatientDetail", kwargs={'pk': self.kwargs["patient_id"]}))
        return super(RecordUpdateView, self).dispatch(request, *args, **kwargs)

@login_required
def SearchPatient(request):
    
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ""
    
    patients = Patient.objects.filter(fullname__contains=search_text)[:5]
    return render_to_response('patient_info/ajax_search.html', {"patients": patients})

class AllPAtientsListView(LoginRequiredMixin, ListView):
    queryset = Patient.objects.filter(hided=False).order_by("-is_active", "fullname",)
    model = Patient
    paginate_by = 20
    context_object_name = "patients"
    template_name = 'patient_info/patients_db.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.request.user)
        context["profile"] = profile.occupation
        return context
