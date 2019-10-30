from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from accounts.models import Profile


class RegistrationProfileForm(forms.ModelForm):
    
    OCCUPATION_CHOICES = [
        ('D', 'Врач'),
        ('N', 'Медперсонал'),
    ]
    
    email = forms.EmailField(max_length=200, help_text="Required", label="Введите рабочую почту")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")
    occupation = forms.ChoiceField(widget=forms.Select, choices=OCCUPATION_CHOICES, label="Специальность")

    class Meta:
        model=User
        fields = ("username", "email")
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают! Попробуйте ввести снова")
        return cd["password2"]
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой зарегистрирован")
        # if email.split("@")[1] != "emcmos.ru":
        #     raise forms.ValidationError("Пожалуйста, введите рабочую почту")
        return email