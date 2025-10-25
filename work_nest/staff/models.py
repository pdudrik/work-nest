from datetime import datetime
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator


PAYCHECK_CHOICES = [
    ("monthly", "Monthly"),
    ("weekly", "Weekly"),
    ("biweekly", "Bi-Weekly"),
]
EMPLOYEE_STATUS_CHOICES = [
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("on_leave", "On leave"),
]
EMPLOYMENT_TYPE_CHOICES = [
    ("part_time", "Part Time"),
    ("full_time", "Full Time"),
    ("internship", "Internship"),
]
TASK_STATUS_CHOICES = [
    ("todo", "To-Do"),
    ("in_progress", "In Progress"),
    ("done", "Done"),
    ("reviewed", "Reviewed"),
]
PROJECT_STATUS_CHOICES = [
    ("not_started_yet", "Not Started Yet"),
    ("in_progress", "In Progress"),
    ("unfinished", "Paused/Unfinished"),
    ("done", "Done"),
]

DEFAULT_PAYCHECK_CHOICE = PAYCHECK_CHOICES[0][0]
DEFAULT_EMPLOYEE_STATUS_CHOICE = EMPLOYEE_STATUS_CHOICES[0][0]
DEFAULT_EMPLOYMENT_TYPE_CHOICE = EMPLOYMENT_TYPE_CHOICES[0][0]
DEFAULT_TASK_STATUS_CHOICE = TASK_STATUS_CHOICES[0][0]
DEFAULT_PROJECT_STATUS_CHOICE = PROJECT_STATUS_CHOICES[0][0]
DEFAULT_EMPLOYEE_PHOTO="staff/not_set.png"


class PersonalProfile(models.Model):
    first_name = models.CharField(
        max_length=50
    )
    middle_name = models.CharField(
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        max_length=50
    )
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - personal profile"


    def get_absolute_url(self):
        return reverse("staff:staff-profile-detail", kwargs={"pk": self.pk})
    

class Employee(models.Model):
    email = models.EmailField(
        max_length=50,
        unique=True
    )
    employee_id = models.CharField(
        max_length=10,
        unique=True
    )
    joined_date = models.DateField()
    photo = models.ImageField(
        default=DEFAULT_EMPLOYEE_PHOTO,
        upload_to="employees/"
    )
    status = models.CharField(
        max_length=15,
        choices=EMPLOYEE_STATUS_CHOICES,
        default=DEFAULT_EMPLOYEE_STATUS_CHOICE
    )
    personal_info = models.OneToOneField(
        "PersonalProfile",
        on_delete=models.CASCADE,
        related_name="employee"
    )

    def __str__(self):
        if self.personal_info:
            return f"{self.personal_info.first_name} {self.personal_info.last_name} - {self.employee_id}"
        return f"Employee {self.employee_id}"

    
    def get_absolute_url(self):
        return reverse("staff:staff-profile-detail", kwargs={"pk": self.pk})
    


class Address(models.Model):
    street = models.CharField(
        max_length=30,
        blank=True
    )
    number = models.CharField(
        max_length=10
    )
    city = models.CharField(
        max_length=30
    )
    country = models.CharField(
        max_length=30
    )
    postal_code = models.CharField(
        max_length=10
    )
    personal_info = models.OneToOneField(
        "PersonalProfile",
        on_delete=models.CASCADE,
        related_name="address"
    )

    def __str__(self):
        if self.personal_info:
            return f"{self.personal_info.first_name} {self.personal_info.last_name} - address"
        return f"Address - {self.city}, {self.street}"


class Employment(models.Model):
    role = models.CharField(
        max_length=20
    )
    started_role_at_date = models.DateField()
    income = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    currency = models.CharField(
        max_length=3,       # allow ISO code only
        default="EUR"
    )
    ending_role_at_date = models.DateField(
        blank=True,
        null=True
    )
    type = models.CharField(
        max_length=15,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=DEFAULT_EMPLOYMENT_TYPE_CHOICE
    )
    notice_period = models.CharField(
        max_length=10
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="employments"
    )

    @property
    def current_employment(self):
        return self.employments.filter(ending_role_at_date__isnull=True).first()

    def __str__(self):
        if self.employee.personal_info:
            return f"{self.employee.personal_info.first_name} {self.employee.personal_info.first_name} - {self.role}"
        return f"Employment - {self.role}"


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee"],
                condition=models.Q(ending_role_at_date__isnull=True),
                name="uniq_current_employment_per_employee"
            )
        ]


class PayrollProfile(models.Model):
    employee = models.OneToOneField(
        "Employee",
        on_delete=models.CASCADE,
        related_name="payroll"
    )
    iban = models.CharField(
        max_length=40,
    )
    paycheck_period = models.CharField(
        max_length=20,
        choices=PAYCHECK_CHOICES,
        default=DEFAULT_PAYCHECK_CHOICE
    )

    def __str__(self):
        if self.employee.personal_info:
            return f"{self.employee.personal_info.first_name} {self.employee.personal_info.first_name} - payroll profile"
        
        elif self.employee:
            return f"{self.employee.employee_id} - payroll profile"
        
        elif self.iban is not None:
            return f"payroll profile - {self.iban[0:4]}...{self.iban[-4:]}"
        
        return "payroll profile - undefined"



class Project(models.Model):
    name = models.CharField(
        max_length=50
    )
    description = models.TextField(
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS_CHOICES,
        default=DEFAULT_PROJECT_STATUS_CHOICE
    )
    created_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="projects_created"
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    participants = models.ManyToManyField(
        Employee,
        through="EmployeeProject",
        related_name="projects",
    )

    def __str__(self):
        return f"Project ({self.status}) - {self.name}"


class Task(models.Model):
    name = models.CharField(
        max_length=50
    )
    description = models.TextField(
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default=DEFAULT_TASK_STATUS_CHOICE
    )
    created_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="tasks_created"
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT
    )
    assigned_employees = models.ManyToManyField(
        Employee,
        through="EmployeeTask",
        related_name="tasks"
    )

    def __str__(self):
        return f"Task ({self.status}) - {self.name}"


class EmployeeProject(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    date_left = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        if self.employee.personal_info:
            return f"{self.employee.personal_info.first_name} {self.employee.personal_info.first_name} - {self.project.name}"

        return f"{self.employee.employee_id} - {self.project.name}"


    # Allow rejoining project and to be joined only once in the project (no dupilcates)
    # Allowed only for PostgreSQL and SQLite 3.8.0+
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "project"],
                condition=models.Q(date_left__isnull=True),
                name="uniq_active_employee_project"
            )
        ]


class EmployeeTask(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    date_left = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        if self.employee.personal_info:
            return f"{self.employee.personal_info.first_name} {self.employee.personal_info.first_name} - {self.task.name}"

        return f"{self.employee.employee_id} - {self.task.name}"


    # Allow rejoining task and to be joined only once in the task (no dupilcates)
    # Allowed only for PostgreSQL and SQLite 3.8.0+
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "task"],
                condition=models.Q(date_left__isnull=True),
                name="uniq_active_employee_task"
            )
        ]
