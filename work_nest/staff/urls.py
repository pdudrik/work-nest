from django.urls import path
from . import views


app_name = "staff"


urlpatterns = [
    path("", views.StaffHomeView.as_view(), name="staff-home"),
    path("add/", views.StaffAddView.as_view(), name="staff-add"),
    path("login/", views.StaffLoginView.as_view(), name="login"),
    path("logout/", views.StaffLogoutView.as_view(), name="logout"),
]