from django.db import models
from django.contrib.auth.models import User
import datetime


class UserInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=20)
    mobile = models.CharField(max_length=25)
    grade = models.CharField(max_length=20)
    school = models.CharField(max_length=25)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    verification_code = models.CharField(max_length=25, default='')

# Create your models here.
