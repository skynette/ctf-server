from django.contrib import admin

# Register your models here.
from .models import LeaderboardUser, Flag

admin.site.register(LeaderboardUser)
admin.site.register(Flag)