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

class Booked(models.Model):
    name = models.CharField(max_length=50)
    roomnumber = models.IntegerField()
    phonenumber = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_id = models.CharField(max_length=50)

class Cleanshifts(models.Model):
    name = models.CharField(max_length=50)
    roomnumber = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
