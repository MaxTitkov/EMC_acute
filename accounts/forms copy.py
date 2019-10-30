from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from accounts.models import Profile


# class LoginForm(forms):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RegistrationProfileForm(forms.ModelForm):

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        cd = self.cleaned_data
        email_endswith = "emcmos.ru"
        entered_email = cd['email']
        if entered_email.split("@")[1] != email_endswith:
            raise forms.ValidationError("Регистрировать можно только на рабочую почту")
        if User.objects.filter(email__iexact=entered_email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        return entered_email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]


    # # occupation = forms.CharField(label = "Выберите вашу должность")
    # password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    # password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    # class Meta:
    #     model = User
    #     fields = ('username',)
    
    # def clean_email(self):
    #     cd = self.cleaned_data
    #     email_endswith = "emcmos.ru"
    #     entered_email = cd['email']
    #     if entered_email.split("@")[1] != email_endswith:
    #         raise forms.ValidationError("Регистрировать можно только на рабочую почту")
    #     if User.objects.filter(email__iexact=entered_email).exists():
    #         raise forms.ValidationError('A user has already registered using this email')
    #     return entered_email
    
    # def save(self, **kwargs):
    #     profile = super().save(commit=False)
    #     user = User.objects.create(username = self.cleaned_data['username'])
    #     profile.user=user
    #     profile.save()
    #     return profile

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd["password"] != cd['password2']:
    #         raise forms.ValidationError("Пароли не совпадают")
    #     return cd["password2"]
