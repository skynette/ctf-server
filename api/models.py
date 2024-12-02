# api/models.py
from django.db import models
import secrets
import string

class UserSession(models.Model):
    username = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_token(cls):
        # Generate a random 32-character token
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))

    @classmethod
    def create_session(cls, username):
        token = cls.generate_token()
        return cls.objects.create(username=username, token=token)
    
    def __str__(self):
        return f"Session: {self.username} (Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"


class LeaderboardUser(models.Model):
    username = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    submitted_flags = models.ManyToManyField('Flag', blank=True)
    
    def __str__(self):
        return f"{self.username} - Points: {self.points}"


class Flag(models.Model):
    value = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.value


class Config(models.Model):
    game_started = models.BooleanField(default=False)
    password = models.CharField(max_length=255, default="gdgbenin")
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Ensure only one config instance exists
        verbose_name = 'Game Configuration'
        verbose_name_plural = 'Game Configuration'

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(pk=1)
        return config

    def __str__(self):
        return f"Game Configuration (Started: {self.game_started})"
