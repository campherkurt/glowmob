from django.contrib import admin
from django.db import models
from django import forms
from apps.story.models import Story, Genre, Chapter, Download, Announcement, Competition, CompetitionEntry, Series, Language, WriteStoryEntry, Review
import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
import re

class CompetitionInline(admin.StackedInline):
    model = Competition
    extra = 1
    
class AnnouncementInline(admin.StackedInline):
    model = Announcement
    extra = 1

class DownloadInline(admin.StackedInline):
    model = Download
    extra = 1
    
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['select_chapter']
    ordering = ('story__title','id')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'review_object', 'is_approved')
    ordering = ['-created']
    readonly_fields = ['user', 'created', 'review_object']
    fieldsets = (
        (None, {
            'fields': ('user', 'review', 'is_approved'),
        }),
    )

class ChapterInline(admin.StackedInline):
    model = Chapter
    fieldsets = (
        (None,{
            'fields': ('title','order', 'poll')
        }),
        ('Content',{
            'classes': ('collapse',),
            'fields':('publish_date','image','short_description','body'),
        })
    )
    extra = 1

    
class StoryAdmin(admin.ModelAdmin):
    list_display = ["title", 'word_count', 'language', 'display_on_homepage', 'is_public']
    list_filter = ["is_public", "display_on_homepage", "genre", "language", "type", "created", "modified", "author", "publisher"]
    inlines = [ChapterInline, DownloadInline, CompetitionInline]

    class Media:
        js = (
            settings.STATIC_URL + "js/jquery-1.3.2.min.js", 
            settings.STATIC_URL + "js/wymeditor/jquery.wymeditor.js",
            settings.STATIC_URL + "js/story_editor.js",
            )
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]

class SeriesAdmin(admin.ModelAdmin):
    list_display = ["title"]

class LanguageAdmin(admin.ModelAdmin):
    list_display = ["language"]

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['created','announcement', 'parent_story']

class CompetitionEntryAdmin(admin.ModelAdmin):
    list_display = ["competition", "user", "name", "number", 'response', 'created']
    list_filter = ['competition', 'created']
    search_fields = ('competition__title',)
    readonly_fields = ('user', 'created',)

class WriteStoryEntryAdmin(admin.ModelAdmin):
    list_display = ["name","email","cellphone","website", "created_at"]
    list_filter = ["created_at",]
    readonly_fields = ('created_at',)
    
class CompetitionAdmin(admin.ModelAdmin):
    class Media:
        js = (
            settings.STATIC_URL + "js/jquery-1.3.2.min.js", 
            settings.STATIC_URL + "js/wymeditor/jquery.wymeditor.js",
            settings.STATIC_URL + "js/story_editor.js",
            )
    list_display = ['title', 'story', 'created', 'active']
    list_filter = ['story', 'created', 'active']

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(CompetitionEntry, CompetitionEntryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(WriteStoryEntry, WriteStoryEntryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Competition, CompetitionAdmin)