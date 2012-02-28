from django.db import models
from django.utils.translation import ugettext_lazy as _

class Contact(models.Model):
    name = models.CharField(_("Your Name"), max_length=255)
    contact = models.CharField(_("Your cellphone number or email address"), max_length=255)
    message = models.TextField(_("Your message"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name