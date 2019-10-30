from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login") ,
    path("logout/", auth_views.LogoutView.as_view(template_name="accounts/logged_out.html"), name="logout"),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='accounts/change-password.html')
    ),
    # path("registration/", views.register, name="Registration"),
    path("registration/", views.registration, name="Registration"),
    path('activate/<slug:uidb64>/<slug:token>)/', views.activate, name='activate'),
]