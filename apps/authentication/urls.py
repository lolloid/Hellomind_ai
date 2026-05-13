from django.urls import path

from .views import LoginView, MeView, RegisterView, SettingsView


urlpatterns = [
    path("register", RegisterView.as_view(), name="auth-register"),
    path("register/", RegisterView.as_view(), name="auth-register-slash"),
    path("login", LoginView.as_view(), name="auth-login"),
    path("login/", LoginView.as_view(), name="auth-login-slash"),
    path("me", MeView.as_view(), name="auth-me"),
    path("me/", MeView.as_view(), name="auth-me-slash"),
    path("settings", SettingsView.as_view(), name="auth-settings"),
    path("settings/", SettingsView.as_view(), name="auth-settings-slash"),
]
