from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


#==============================================================================
class Featured(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(_('Title'), max_length=255)
    content_type = models.ForeignKey(ContentType,
        limit_choices_to = {"model__in": ("story", "chapter")}, )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")

    def __unicode__(self):
        return self.title
    
    def featured_item(self):
        if self.content_type.model == 'chapter':
            return '%s - %s' % (self.content_object.story.title, self.content_object.title)
        else:
            return self.content_object
    
    
        