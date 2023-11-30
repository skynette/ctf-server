# api/serializers.py
from rest_framework import serializers
from .models import LeaderboardUser

class LeaderboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderboardUser
        fields = ['username', 'points']
