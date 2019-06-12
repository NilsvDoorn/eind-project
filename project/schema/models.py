from django.db import models

# Create your models here.
class Rooms(models.Model):
    roomnumber = models.IntegerField(unique=True)
    luxe = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=6)

class Reviews(models.Model):
    anoniem = models.BooleanField(null=True, blank=True)
    name = models.CharField(max_length=50)
    note = models.IntegerField()
    message = models.CharField(max_length=200)
    roomnumber = models.IntegerField()

class Chat(models.Model):
    name = models.CharField(max_length=50)
    roomnumber = models.IntegerField()
    message = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)

class Clipped(models.Model):
    name_staff = models.CharField(max_length=50)
    name_user = models.CharField(max_length=50)
    roomnumber = models.IntegerField()
    message = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)

class Booked(models.Model):
    name = models.CharField(max_length=50)
    roomnumber = models.IntegerField()
    phonenumber = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

class Cleanshifts(models.Model):
    name = models.CharField(max_length=50)
    roomnumber = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
