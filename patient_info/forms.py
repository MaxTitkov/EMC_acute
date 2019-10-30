from django import forms
from .models import Patient, Info

class AddPatientForm(forms.Form):
    class Meta:
        model = Patient
        fields = ("fullname", "dob", "room",)
        labels = {"fullname": "ФИО", "dob": "Дата рождения", "room": "Палата"}

class AddRecordForm(forms.ModelForm):
    # bathroom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-range', 'type': 'range', "min": "1", "max": "60", "step": "0,17"}))
    class Meta:
        model = Info
        fields = ("suicidal_risk", "bathroom_time", "record", "patient", "bathroom_time",)
        labels = {"suicidal_risk": "Суицидальный риск", "record": "Комментарии", "bathroom_time": "Время в туалете"}
        widgets = {'patient': forms.HiddenInput(),
                    "suicidal_risk": forms.RadioSelect(attrs={'class':"suicidal"}),
                    "record": forms.Textarea(attrs={'class':"text_cls"}),
                    }