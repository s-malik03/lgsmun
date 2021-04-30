from django.db import models
from django.contrib.auth.models import User


class UserCommittee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    committee = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Attendance(models.Model):
    country = models.CharField(max_length=100)
    committee = models.CharField(max_length=50)
    status = models.CharField(default='Absent', max_length=50)
    recognized = models.IntegerField(default=0)
    placard = models.CharField(default='', max_length=20)


class GSL(models.Model):
    country = models.CharField(max_length=100)
    committee = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class RSL(models.Model):
    country = models.CharField(max_length=100)
    committee = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class Notifications(models.Model):
    country = models.CharField(max_length=100)
    committee = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class FloorMods(models.Model):
    mod = models.TextField()
    committee = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    committee = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)


class CommitteeControl(models.Model):
    committee = models.CharField(max_length=100, primary_key=True)
    speaking_mode = models.CharField(default='Idle', max_length=100)
    topic = models.CharField(default='No Topic Has Been Set', max_length=100)
    current_mod = models.CharField(default='No Moderated Caucus in Progress', max_length=100)
    zoom_link = models.CharField(default='', max_length=100)
    drive_link = models.CharField(default='', max_length=100)
    iteration = models.IntegerField(default=0)


class Vote(models.Model):
    committee = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    vote_status = models.CharField(max_length=50)


class Timer(models.Model):
    committee = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='stop')
    duration = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)

# Create your models here.
