# api/urls.py
from django.urls import path
from .views import SubmitFlagView, LeaderboardView, GameControlView, RegisterUserView

urlpatterns = [
     path('register/', RegisterUserView.as_view(), name='register'),
    path('game-control/', GameControlView.as_view(), name='game-control'),
    path('submit-flag/', SubmitFlagView.as_view(), name='submit_flag'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
