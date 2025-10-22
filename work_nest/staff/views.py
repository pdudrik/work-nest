from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib import messages


# def staff_home_view(request):
#     return render(request, "staff/staff-home.html")


# def staff_add_view(request):
#     return render(request, "staff/staff-add.html")


class StaffHomeView(TemplateView):
    template_name = "staff/staff-home.html"

class StaffAddView(TemplateView):
    template_name = "staff/staff-add.html"


class StaffLoginView(LoginView):
    template_name = "staff/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        remember_me = self.request.POST.get("remember_me")

        if remember_me:
            self.request.session.set_expiry(None)
        
        else:
            self.request.session.set_expiry(0)      # expire when the browser closes

        return response
    

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("staff:staff-home")
    

class StaffLogoutView(LogoutView):    
    next_page = reverse_lazy("staff:login")


    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
    

    def post(self, request, *args, **kwargs):
        messages.success(request, "Logged out successfully")
        return super().post(request, *args, **kwargs)