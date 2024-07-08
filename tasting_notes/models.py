# models.py
from django.db import models

class UserContact(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class UserResidence(models.Model):
    name = models.CharField(max_length=255)
    room_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name



