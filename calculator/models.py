from django.db import models


class City(models.Model):
    auction = models.CharField(max_length=6)
    city = models.CharField(max_length=50)
    seaport = models.CharField(max_length=2)
    price = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city




