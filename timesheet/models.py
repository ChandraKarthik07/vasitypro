


from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import uuid
import datetime
import pytz
from django.utils.translation import gettext_lazy as _
class CustomUserManager(UserManager):
    pass

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email=models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the form of +919999999999.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    # otp = models.CharField(max_length=6, null=True, blank=True)
    google_extra_data =models.TextField(null=True, blank=True)
    objects = CustomUserManager()
    # USERNAME_FIELD="email"
    # REQUIRED_FIELDS=[]

    def __str__(self):
        return f"{self.username}-{self.id}"
    class meta:
        db_table = 'User'


User._meta.get_field('groups').remote_field.related_name = 'user_replica_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_replica_permissions'

# from django.contrib.auth import get_user_model
# User = get_user_model() 

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,to_field='id')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    project_instance_created_date = models.DateTimeField(auto_now_add=True)
    estimated_duration = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)  # Use ManyToManyField for multiple projects
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    week_start_date = models.DateField(blank=True, null=True)  
    def __str__(self):
        return f"{self.user.username}'s Timesheet for {self.project.name} starting {self.week_start_date}"