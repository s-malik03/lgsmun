from django.db import models
from django.contrib.auth.models import User


class UserInformation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    mobile = models.CharField(max_length=25)
    grade = models.CharField(max_length=20)
    school = models.CharField(max_length=25)

# Create your models here.
