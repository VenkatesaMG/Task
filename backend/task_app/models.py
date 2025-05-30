from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q
import string
import random

ROLES = [
    ("admin", "Admin"),
    ("lead", "Lead"),
    ("member", "Member"),
    ("purchaser", "Purchaser")
]

PRIORITY = [
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low")
]

STATUS = [
    ("raised", "Raised"),
    ("approved", "Approved"),
    ("in progress", "In Progress"),
    ("delivered", "Delivered")
]

def generate_unique_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length = 25, choices=ROLES)
    user_id = models.CharField(max_length = 6, unique=True, blank = False, editable=False)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField()
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.user_id:
            while True:
                code = generate_unique_code()
                if not User.objects.filter(user_id=code).exists():
                    self.user_id = code
                    break
        super().save(*args, **kwargs)

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    # project_lead = models.ForeignKey(User, blank=True, null=True)
    project_name = models.CharField(max_length=25)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.FloatField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lte = models.F('end_date')), name='start_before_end')
        ]

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=25)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY)
    status = models.CharField(max_length=20, choices=STATUS)
    deadline = models.DateField()

    def clean(self):
        if self.deadline > self.project.end_date:
            raise ValidationError("Task deadline must be on or before the project's end date.")

class Supplier(models.Model):
    supplier_org = models.CharField(max_length=25, unique=True)

class Purchase(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    products = models.JSONField(default=list)
    raised_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases_raised'
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases_reviewed', blank=True, null=True
    )
    status = models.CharField(choices=STATUS, max_length=25)
    date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)