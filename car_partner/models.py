from django.db import models
from unixtimestampfield.fields import UnixTimeStampField


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=180)
    address = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    created_at = UnixTimeStampField(auto_now_add=True, use_numeric=True)
    modified_at = UnixTimeStampField(auto_now=True, use_numeric=True)
    deleted_at = UnixTimeStampField(null=True, blank=True, use_numeric=True)


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    average_fuel = models.FloatField()
    delegation_starting = UnixTimeStampField()
    delegation_ending = UnixTimeStampField()
    driver = models.CharField(max_length=160)
    owner = models.CharField(max_length=160)
    type = models.CharField(max_length=20)
    partners = models.ManyToManyField(Partner, blank=True, related_name='cars_set', editable=False)
    created_at = UnixTimeStampField(auto_now_add=True, use_numeric=True)
    modified_at = UnixTimeStampField(auto_now=True, use_numeric=True)
    deleted_at = UnixTimeStampField(null=True, blank=True, use_numeric=True)
