from django.db import models

class User(models.Model):

    email=models.CharField(max_length=100,primary_key=True)
    real_name=models.CharField(default="none",max_length=100)
    password=models.CharField(max_length=200)
    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=100)
    school=models.CharField(max_length=100)
    role=models.CharField(default="delegate",max_length=100)

# Create your models here.
