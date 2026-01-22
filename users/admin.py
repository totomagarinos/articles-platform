from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
  list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

  list_filter = ('role', 'is_staff', 'is_active')

  fieldsets = UserAdmin.fieldsets + (
    ('Información Extra', {'fields': ('role', 'bio', 'profile_picture')}),
  )
