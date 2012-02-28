from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from apps.basic_profiles.models import Profile

class InlineProfileAdmin(admin.StackedInline):
    model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [InlineProfileAdmin]
    search_fields = ['first_name', 'last_name', 'username', 'profile__name', 'profile__mobile']


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin )