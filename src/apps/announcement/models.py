from django.db import models
from django.utils.translation import ugettext_lazy as _

class Announcement(models.Model):
    announcement = models.CharField(_("Announcement"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.announcement