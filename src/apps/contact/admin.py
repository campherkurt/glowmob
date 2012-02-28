from django.contrib import admin
from apps.contact.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "contact", 'created']
    list_filter = ['created']
    readonly_fields = ['created']

admin.site.register(Contact, ContactAdmin)