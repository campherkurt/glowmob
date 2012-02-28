from django.contrib import admin
from apps.static_pages.models import Page
from apps.story.models import Story
import settings

class PageAdmin(admin.ModelAdmin):
    list_display = ["title"]
    
    class Media:
        js = (
            settings.STATIC_URL + "js/jquery-1.3.2.min.js", 
            settings.STATIC_URL + "js/editor.js",
            settings.STATIC_URL + "js/wymeditor/jquery.wymeditor.js"
            )
admin.site.register(Page, PageAdmin)
