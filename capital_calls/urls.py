from django.urls import path
from . import views

app_name = "capital_calls"
urlpatterns = [
    path("", views.WelcomeView.as_view(), name="welcome"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("new-call", views.NewCallView.as_view(), name="new_call"),
]
