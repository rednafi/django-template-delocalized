from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=255)
    age = models.FloatField(max_length=5)
    height = models.FloatField(max_length=5)
