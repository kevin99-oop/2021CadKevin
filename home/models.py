from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CovidDb(models.Model):
    Name = models.CharField(max_length=100)
    Oxy = models.IntegerField()
    Pulse = models.IntegerField()
    Temp = models.IntegerField()
    result = models.CharField(max_length=100)

class diabDb(models.Model):
    name = models.CharField(max_length=100)
    glucose = models.IntegerField()
    bloodpressure = models.IntegerField()
    skinthickness = models.IntegerField()
    bmi = models.IntegerField()
    insulin = models.IntegerField()
    pedigree = models.IntegerField()
    age = models.IntegerField()
    result1 = models.CharField(max_length=100)

class alco(models.Model):
    Name1 = models.CharField(max_length=100)
    Age = models.IntegerField()
    bac_val = models.FloatField()
    result2 = models.CharField(max_length=100)

