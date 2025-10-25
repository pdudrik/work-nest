from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from .forms import PersonalProfileForm, AddressForm,    \
    StaffLoginForm
from .models import PersonalProfile


class StaffHomeView(ListView):
    template_name = "staff/staff-home.html"
    model = PersonalProfile
    context_object_name = "employees"
    paginate_by = 5

    def get_queryset(self):
        return (
            PersonalProfile.objects
            .only("id", "first_name", "middle_name", "last_name")
            .order_by("last_name", "first_name")
        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop("page", None)
        context["qs_no_page"] = params.urlencode()
        
        return context


    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        
        except Exception:
            # Handle fallback if user tries to access next page which not exist
            qs = self.get_queryset()
            paginator = Paginator(qs, self.paginate_by)
            last = paginator.num_pages or 1
            
            return redirect(f"{request.path}?page={last}")

        

class StaffAddView(TemplateView):
    # form = PersonalProfileForm()
    template_name = "staff/staff-add.html"
    personal_form = PersonalProfileForm
    address_form = AddressForm

    def get_context_data(self,*args, **kwargs):
        context = super(StaffAddView, self).get_context_data(*args,**kwargs)
        if "personal_form" not in context:
            context["personal_form"] = self.personal_form(instace=self.object)
        if "address_form" not in context:
            context["address_form"] = self.address_form(instance=self.object.address)
            
        return context

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "personal_form": self.personal_form,
                "address_form": self.address_form
            }
        )
    
    
    def post(self, request, *args, **kwargs):
        p_form = self.personal_form(request.POST)
        a_form = self.address_form(request.POST)

        if p_form.is_valid() and a_form.is_valid():
            personal_profile = p_form.save()
            print(personal_profile)
            a_form.instance.personal_info = personal_profile
            a_form.save()

            print("SUCCESS: Personal profile and address saved!")

        return redirect("staff:staff-add")
    

class StaffProfileDetail(DetailView):
    template_name="staff/profile-detail.html"
    model = PersonalProfile
    context_object_name = "employee"


    def get_queryset(self):
        return PersonalProfile.objects.select_related("address")






class StaffLoginView(LoginView):
    template_name = "staff/login.html"
    authentication_form = StaffLoginForm
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