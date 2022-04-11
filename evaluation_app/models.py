from django.db import models

# Create your models here.
class Metrics(models.Model):
    field_type=models.CharField(max_length=50)
    pred=models.CharField(max_length=50)
    