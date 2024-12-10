from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),  # Home page for Core module
    path("users/", views.users, name="users"),  # User management page
    path("devices/", views.devices, name="devices"),  # Device management page
    path("schedules/", views.schedules, name="schedules"),  # Schedule management page
    path("generate-recommendations/", views.generate_recommendations_view, name="generate_recommendations"),  # Generate recommendations

]
