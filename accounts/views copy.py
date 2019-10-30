# https://achiengcindy.com/blog/2019/01/17/registration-django-email-confirmation/

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from accounts.forms import RegistrationProfileForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from .tokens import account_activation_token


def registration(request):
    if request.method == "POST":
        registerForm = RegistrationProfileForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            # get current site
            current_site = get_current_site(request)
            subject = 'Активируйте ваш аккаунт'
            # create Message
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                'token': account_activation_token.make_token(user),
            })
            html_message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                'token': account_activation_token.make_token(user),
            })
            # send activation link to the user
            user.email_user(subject=subject, message=message,
                            html_message=html_message)
            return HttpResponse('Письмо с подтверждением регистрации отправлено на почту.')
    else:
        registerForm = RegistrationProfileForm()
    return render(request, "accounts/register.html", {"form": registerForm})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'accounts/account_activation_invalid.html')






# def registration(request):
#     if request.method == "POST":
#         form = RegistrationProfileForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data["password"])
#             new_user.save()
#             return render(request, "accounts/registration_complete.html", {'new_user': new_user})
#     else:
#         form = RegistrationProfileForm()
    
#     return render(request, "accounts/register.html", {'user_form': form})





# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created successfully')
#             return redirect(reverse_lazy("PatientsActiveList"))
#     else:
#         form = UserCreationForm()
#     return render(request, "accounts/register.html", {"form": form})




# from accounts.forms import LoginForm

# class LoginView(View):
#     def post(self, request, *args, **kwargs):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 request,
#                 username=cd['username'],
#                 password = cd['password']
#             )
#             if user is None:
#                 return HttpResponse("Неправильный логин или пароль")
#             if not user.is_active:
#                 return HttpResponse("Ваш аккаунт заблокирован")

#             login(request, user)
#             return HttpResponse("Успешный вход")
#         return render(request, "accounts/login.html", {"form": form})

#     def get(self, request, *args, **kwargs):
#         form = LoginForm()
#         return render(request, "accounts/login.html", {'form': form})

