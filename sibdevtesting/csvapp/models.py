from django.db import models


class Entry(models.Model):
    customer = models.CharField(max_length=255)
    item = models.CharField(max_length=100)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()