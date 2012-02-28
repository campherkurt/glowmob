
from django.contrib import admin
from apps.polls.models import Poll, Choice
import settings

class ChoiceInline(admin.TabularInline):
    model = Choice
    exclude = ('votes',)

class PollAdmin(admin.ModelAdmin):
   list_display = ["question",'poll_results']
   exclude = ('voted',)
   inlines = [ChoiceInline]
   
   class Media:
       js = (
           settings.STATIC_URL + "pinax/js/jquery-1.3.2.min.js", 
           settings.STATIC_URL + "js/collapse.js",
           )

admin.site.register(Poll, PollAdmin)
