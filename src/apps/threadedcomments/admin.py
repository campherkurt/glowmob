from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from threadedcomments.models import ThreadedComment, FreeThreadedComment
import threadedcomments.models


def approve(modeladmin, request, queryset):
    queryset.update(status=threadedcomments.models.STATUS_APPROVED)
    
approve.short_description = "Mark selected comments as Approved"


class ThreadedCommentAdmin(admin.ModelAdmin):
    fieldsets = (
        #(None, {'fields': ('content_type', 'object_id')}),
        #(_('Parent'), {'fields' : ('parent',)}),
        #(_('Content'), {'fields': ('user', 'comment', 'name', 'cellphone')}),
        (_('Content'), {'fields': ('user', 'comment')}),
        #(_('Meta'), {'fields': ('is_public', 'date_submitted', 'date_modified', 'date_approved', 'is_approved', 'ip_address')}),
        (_('Meta'), {'fields': ('date_submitted', 'date_modified', 'status')}),
    )
    list_display = ('date_submitted', 'content_type', 'get_content_object_str', 'comment', 'name', 'cellphone', 'status')
    list_filter = ('date_submitted','status')
    readonly_fields = ['user']
    date_hierarchy = 'date_submitted'
    search_fields = ('comment', 'user__username')
    actions = [approve]

class FreeThreadedCommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('content_type', 'object_id')}),
        (_('Parent'), {'fields' : ('parent',)}),
        (_('Content'), {'fields': ('name', 'website', 'email', 'comment')}),
        (_('Meta'), {'fields': ('date_submitted', 'date_modified', 'date_approved', 'is_public', 'ip_address', 'is_approved')}),
    )
    list_display = ('name', 'date_submitted', 'content_type', 'get_content_object', 'parent', '__unicode__')
    list_filter = ('date_submitted','is_approved')
    date_hierarchy = 'date_submitted'
    search_fields = ('comment', 'name', 'email', 'website')


admin.site.register(ThreadedComment, ThreadedCommentAdmin)
#admin.site.register(FreeThreadedComment, FreeThreadedCommentAdmin)
