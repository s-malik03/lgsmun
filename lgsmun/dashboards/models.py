from django.db import models

class Attendance(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)
    status=models.CharField(default='Absent',max_length=50)
    recognized=models.IntegerField(default=0)
    placard=models.CharField(default='',max_length=20)

class GSL(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)
    date=models.DateField(auto_now_add=True)

class RSL(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)
    date=models.DateField(auto_now_add=True)

class Notifications(models.Model):

    country=models.CharField(max_length=100)
    committee=models.CharField(max_length=50)
    message=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)

class Messages(models.Model):

    committee=models.CharField(max_length=100)
    sender=models.CharField(max_length=100)
    recipient=models.CharField(max_length=100)
    message=models.CharField(max_length=250)
    date=models.DateField(auto_now_add=True)

class CommitteeControl(models.Model):

    committee=models.CharField(max_length=100,primary_key=True)
    speaking_mode=models.CharField(default='Idle',max_length=100)
    allow_motions=models.BooleanField()
    topic=models.CharField(default='No Topic Has Been Set',max_length=100)
    current_mod=models.CharField(default='No Moderated Caucus in Progress',max_length=100)

class Mods(models.Model):

    committee=models.CharField(max_length=100)
    topic=models.CharField(max_length=100)
    date=models.DateField(aut_now_add=True)

class Vote(models.Model):

    committee=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    vote_status=models.CharField(max_length=50)

# Create your models here.
