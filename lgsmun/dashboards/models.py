from django.db import models

class Attendance(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)
    status=models.CharField(default='Absent',max_length=50)
    recognized=models.IntegerField(default=0)

class GSL(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)

class RSL(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)

# Create your models here.
