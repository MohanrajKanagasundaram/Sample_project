from django.db import models

class Procedure(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Section(models.Model):
    name=models.CharField(max_length=50)
    procedure=models.ForeignKey(Procedure,on_delete=models.CASCADE,related_name='section')
    def __str__(self):
        return self.name

class Field(models.Model):
    id=models.IntegerField(primary_key=True)
    label=models.CharField(max_length=50)
    section=models.ForeignKey(Section,on_delete=models.CASCADE,related_name='field')
    type=models.CharField(max_length=50)
    options=models.CharField(max_length=100)
    is_table=models.BooleanField(default=False)
    validations=models.CharField(max_length=50)
    target=models.BooleanField(default=False)
    def __str__(self):
        return self.label