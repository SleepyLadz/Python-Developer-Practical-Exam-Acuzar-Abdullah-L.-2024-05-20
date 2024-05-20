from django.db import models


# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    position = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.color} {self.position}'
