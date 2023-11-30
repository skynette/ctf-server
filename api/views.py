# api/views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import LeaderboardUser
from .serializers import LeaderboardUserSerializer

class SubmitFlagView(generics.CreateAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer

class LeaderboardView(generics.ListAPIView):
    queryset = LeaderboardUser.objects.all()
    serializer_class = LeaderboardUserSerializer
