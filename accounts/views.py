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

from accounts.models import Profile
from django.contrib.auth.models import Group

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from .tokens import account_activation_token
from django.contrib.auth.models import User


def registration(request):
    if request.method == "POST":
        registerForm = RegistrationProfileForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            # Set Profile and UserGroup according this
            profile = Profile.objects.get_or_create(user=user, occupation=registerForm.cleaned_data['occupation'])
            if registerForm.cleaned_data['occupation'] == "D":
                doctor_group = Group.objects.get(name='Doctor')
                doctor_group.user_set.add(user)
            else:
                nurse_group = Group.objects.get(name='Nurse')
                nurse_group.user_set.add(user)


            # get current site
            current_site = get_current_site(request)
            subject = 'Активируйте ваш аккаунт'
            # create Message
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            html_message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # send activation link to the user
            user.email_user(subject=subject, message=message,
                            html_message=html_message)
            return render(request, "accounts/confirmation_sent.html", {"user": user})
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