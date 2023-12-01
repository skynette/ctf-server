# api/serializers.py
from rest_framework import serializers
from .models import LeaderboardUser

class LeaderboardUserSerializer(serializers.ModelSerializer):
    flag = serializers.CharField(write_only=True)
    
    class Meta:
        model = LeaderboardUser
        fields = ['username', 'points', 'flag']
        read_only_fields = ['points']
