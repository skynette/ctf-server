# api/models.py
from django.db import models

class LeaderboardUser(models.Model):
    username = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    submitted_flags = models.ManyToManyField('Flag', blank=True)

class Flag(models.Model):
    value = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.value
