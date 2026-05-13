from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("login", TemplateView.as_view(template_name="login.html"), name="login-page"),
    path("dashboard", TemplateView.as_view(template_name="dashboard.html"), name="dashboard-page"),
    path("auth/", include("apps.authentication.urls")),
    path("", include("apps.chat.urls")),
    path("mood/", include("apps.mood.urls")),
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/", include("apps.chat.urls")),
    path("api/v1/mood/", include("apps.mood.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
]
