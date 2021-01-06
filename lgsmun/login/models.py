from django.db import models

class User(models.Model):

    email=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=100)
    school=models.CharField(max_length=100)

# Create your models here.
