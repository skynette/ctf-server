# api/models.py
from django.db import models

class LeaderboardUser(models.Model):
    username = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
