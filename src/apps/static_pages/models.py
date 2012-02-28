from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import apps.static_pages.constants

from apps.story.models import Story

#==============================================================================
class Page(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    title = models.CharField(_("Title"),max_length=200)
    content = models.TextField(blank=False)
    image = models.ImageField(upload_to='static', blank=True, null=True)
    type = models.IntegerField(choices=apps.static_pages.constants.STATIC_PAGES_TYPE_CHOICES)
    story = models.ManyToManyField(Story, blank=True, null=True)
    
    #--------------------------------------------------------------------------
    def __unicode__(self):
        return self.title
