from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_suspended', 'created_at']
    list_filter = ['is_suspended', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('phone', 'is_suspended', 'suspended_until')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'reputation_score', 'level', 'total_wins']
    list_filter = ['level']
    search_fields = ['user__username', 'user__email']