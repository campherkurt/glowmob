from django.contrib import admin
from apps.announcement.models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["announcement"]

admin.site.register(Announcement, AnnouncementAdmin)