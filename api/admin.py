# api/admin.py
from django.contrib import admin
from .models import UserSession, LeaderboardUser, Flag, Config


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('username', 'token', 'created_at')
    search_fields = ('username', 'token')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(LeaderboardUser)
class LeaderboardUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'points', 'flag_count')
    search_fields = ('username',)
    filter_horizontal = ('submitted_flags',)
    ordering = ('-points',)

    def flag_count(self, obj):
        return obj.submitted_flags.count()
    flag_count.short_description = 'Submitted Flags'

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ('value', 'points', 'submission_count')
    search_fields = ('value',)
    ordering = ('value',)

    def submission_count(self, obj):
        return LeaderboardUser.objects.filter(submitted_flags=obj).count()
    submission_count.short_description = 'Times Submitted'

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('game_started', 'start_time', 'end_time')
    readonly_fields = ('start_time', 'end_time')

    def has_add_permission(self, request):
        # Prevent creating additional config instances
        return Config.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the config
        return False