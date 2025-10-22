from django.contrib import admin
from .models import PersonalProfile, Employee, Address, \
    Employment, PayrollProfile, Project, Task, \
    EmployeeProject, EmployeeTask


# Register your models here.
admin.site.register(PersonalProfile)
admin.site.register(Employee)
admin.site.register(Address)
admin.site.register(Employment)
admin.site.register(PayrollProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(EmployeeProject)
admin.site.register(EmployeeTask)