from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import PersonalProfile, Employee, Address, \
    Employment, PayrollProfile, Project, Task


class StaffLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control form-control-lg"
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control form-control-lg"
        })


class PersonalProfileForm(forms.ModelForm):

    class Meta:
        model = PersonalProfile
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class":"form-control input-width col-9"
            }),
            "middle_name": forms.TextInput(attrs={""
                "class":"form-control input-width col-9"
            }),
            "last_name": forms.TextInput(attrs={
                "class":"form-control input-width col-9"
            }),
            "date_of_birth": forms.DateInput(attrs={
                "class":"form-control input-width col-9",
                "type": "date"
            }),
        }


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = "__all__"



class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ("street", "number", "city", "country", "postal_code",)
        widgets = {
            "street": forms.TextInput(attrs={
                "class": "form-control input-width col-9"
            }),
            "number": forms.TextInput(attrs={
                "class": "form-control input-width col-9"
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control input-width col-9"
            }),
            "country": forms.TextInput(attrs={
                "class": "form-control input-width col-9"
            }),
            "postal_code": forms.TextInput(attrs={
                "class": "form-control input-width col-9"
            }),
        }



class EmploymentForm(forms.ModelForm):
    
    class Meta:
        model = Employment
        fields = "__all__"



class PayrollProfileForm(forms.ModelForm):
    
    class Meta:
        model = PayrollProfile
        fields = "__all__"



class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = "__all__"



class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = "__all__"
























