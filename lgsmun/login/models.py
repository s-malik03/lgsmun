from django.db import models

class User(models.Model):

    email=models.CharField(max_length=100,primary_key=True)
    real_name=models.CharField(default="none",max_length=100)
    password=models.CharField(max_length=200)
    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=100)
    old_committee=models.CharField(max_length=100,default='none')
    school=models.CharField(max_length=100)
    role=models.CharField(default="delegate",max_length=100)
    uuid=models.CharField(max_length=100,default='none')

# Create your models here.
