from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from apps.story.models import Story, Chapter

REGIONS = (
    (1, 'Eastern Cape'),
    (2, 'Free State'),
    (3, 'Gauteng'),
    (4, 'Kwazulu Natal'),
    (5, 'Limpopo'),
    (6, 'Mpumalanga'),
    (7, 'North West'),
    (8, 'Northern Cape'),
    (9, 'Western Cape'),
    (10, 'Not from South Africa'),
)
USER_TYPE_MOBI = 1
USER_TYPE_MXIT = 2

USER_TYPE_CHOICES =(
    (USER_TYPE_MOBI,'Mobi'),
    (USER_TYPE_MXIT, 'MXit')
)
class Profile(models.Model):
    
    user = models.ForeignKey(User, unique=True, verbose_name=_("user"))
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)
    mobile = models.CharField(_('mobile number'), max_length=14, null=True, blank=True)
    birth_date = models.DateField(_('Date of Birth'), null=True)
    region = models.SmallIntegerField(null=True, choices=REGIONS)
    city = models.CharField(_('City/Town'), max_length=255, null=True, blank=True)
    user_type = models.IntegerField(_('User Type'),null=True, choices=USER_TYPE_CHOICES)
    last_story = models.ForeignKey(Story, null=True)
    last_chapter = models.ForeignKey(Chapter, null=True)
    display_mxit_images = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        permissions = (
            ('export', 'Can export profiles'),
        )
        
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"username": self.user.username})


def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_profile, sender=User)
