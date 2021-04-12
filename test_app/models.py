from django.db import models
from django_pendulum_field.model import PendulumField

__all__ = [
    "Something",
    "SomethingWithAutoNow",
    "SomethingWithAutoNowAdd",
]


class Something(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    some_dt = PendulumField()


class SomethingWithAutoNow(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    some_dt = PendulumField(auto_now=True)


class SomethingWithAutoNowAdd(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    dummy_field = models.CharField(max_length=4, default="hi")
    some_dt = PendulumField(auto_now_add=True)
