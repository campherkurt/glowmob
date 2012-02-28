
from django.contrib import admin
from apps.general.models import Featured
import settings


class FeaturedAdmin(admin.ModelAdmin):
    list_display = ['title','content_type', 'featured_item']
    #readonly_fields = ['object_id', ]
    class Media:
        js = (settings.STATIC_URL + "js/jquery-1.3.2.min.js", )
        
admin.site.register(Featured, FeaturedAdmin)