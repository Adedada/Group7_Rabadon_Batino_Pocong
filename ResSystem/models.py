from email import feedparser
from django.db import models
from django.contrib.auth.models import AbstractUser



class Room(models.Model):
    roomID = models.AutoField(primary_key=True)
    status = models.CharField(max_length= 100)
    reservationfee = models.IntegerField()
    date = models.DateField(null=True)
    starttime = models.CharField(max_length= 100)
    endtime = models.CharField(max_length= 100)
    client = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100)

class Agent(AbstractUser):
    agentID = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length= 100)
    lastname = models.CharField(max_length= 100)
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=100)

    class meta:
        db_table = 'tblagent'

