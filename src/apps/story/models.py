from django.db import models
from django.utils.translation import ugettext_lazy as _
import os.path
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.contenttypes.models import ContentType
from apps.polls.models import Poll
import re

DOWNLOAD_CHOICES = (
    ('image', 'Image'),
    ('video', 'Video'),
    ('ringtone', 'Ring Tone')
)

STORY_CHOICES = (
    ('normal', 'Normal'),
    ('classic', 'Yoza Classic'),
)

class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Series(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    banner = models.ImageField(upload_to='series')
    logo = models.ImageField(upload_to=os.path.join('series', 'logo'))
    description = models.TextField(_('Description'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

class Language(models.Model):
    language = models.CharField(_("Title"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.language

class PublicStoryManager(models.Manager):
    
    def get_query_set(self, *args, **kwargs):
        return super(PublicStoryManager, self) \
                    .get_query_set(*args, **kwargs).filter(is_public=True)

class Story(models.Model):
    
    genre = models.ForeignKey(Genre)
    series = models.ForeignKey(Series, blank=True, null=True)
    is_public = models.BooleanField(_("Is public on Yoza"), default=True)
    language = models.ForeignKey(Language)
    title = models.CharField(_("Title"), max_length=255)
    short_description = models.TextField(_("Short Description"))
    author = models.CharField(_("Author"), max_length=255)
    author_url = models.URLField(blank=True, verify_exists=False, null=True)
    publisher = models.CharField(_("Publisher"), max_length=255, blank=True, null=True)
    publisher_url = models.URLField(blank=True, verify_exists=False, null=True)
    image = models.ImageField(upload_to='stories', blank=True, null=True)
    type = models.CharField(_('Type'), max_length=7, choices=STORY_CHOICES)
    word_count = models.IntegerField(_('Word Count'), blank=True, null=True)
    display_on_homepage = models.BooleanField(_('Include in latest on homepage'), default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    poll = models.ForeignKey(Poll, blank=True, null=True)
    is_finished = models.BooleanField(_("The story is finished"))

    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        permissions = (
            ('export', 'Can export story stats'),
        )
    
    objects = models.Manager()
    public = PublicStoryManager()
    
    @property
    def comment_set(self):
        from apps.threadedcomments.models import ThreadedComment
        return ThreadedComment.public.all_for_object(self)
    
    @property
    def stat_set(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        return Stat.objects.filter(content_type=ctype, object_id=self.pk)

#    def save(self, *args, **kwargs):
#        super(Story, self).save(*args, **kwargs)
#        print Chapter.objects.filter(story__id=self.id)


class Chapter(models.Model):
    from apps.polls.models import Poll
    
    story = models.ForeignKey(Story)
    title = models.CharField(_("Title"), max_length=255)
    order = models.IntegerField()
    short_description = models.TextField(_("Short Description"), blank=True, null=True)
    body = models.TextField(_("Body"))
    image = models.ImageField(upload_to=os.path.join('stories', 'chapters'), blank=True, null=True)
    publish_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    poll = models.ForeignKey(Poll, blank=True, null=True)

    def __unicode__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        super(Chapter, self).save(*args, **kwargs)
        story = self.story
        w_c = 0
        chapters = story.chapter_set.all()

        for chapter in chapters:
            body = re.sub("(<([^>]+)>)", "", chapter.body)
            body = re.sub("\s+", " ", body)
            word_count = len(body.strip().split(" "))

            w_c += word_count
        story.word_count = w_c
        story.save()
    
    def select_chapter(self):
        """ For admin display purpose when selecting a chapter"""
        return '%s - %s' % (self.story, self.title)
    
    @property
    def comment_set(self):
        from apps.threadedcomments.models import ThreadedComment
        return ThreadedComment.public.all_for_object(self)
    
    @property
    def stat_set(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        return Stat.objects.filter(content_type=ctype, object_id=self.pk)
    
    class Meta:
        ordering = ['order','created', 'id'] 
        
        
class Stat(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Download(models.Model):
    story = models.ForeignKey(Story)
    title = models.CharField(_("Title"), max_length=255)
    type = models.CharField(_('Type'), max_length=8, choices=DOWNLOAD_CHOICES)
    download = models.FileField(upload_to=os.path.join('stories', 'downloads'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class Announcement(models.Model):
    story = models.ForeignKey(Story, blank=True, null=True)
    announcement = models.CharField(_("Announcement"), max_length=255)
    body = models.TextField(_("Body"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.announcement
    
    def parent_story(self):
        return self.story

class ActiveCompetitionManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCompetitionManager, self) \
                .get_query_set().filter(active=True)

class Competition(models.Model):
    story = models.ForeignKey(Story, blank=True, null=True)
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_('Description'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    visible = ActiveCompetitionManager()
    
    def __unicode__(self):
        return self.title

class CompetitionEntry(models.Model):
    competition = models.ForeignKey(Competition)
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=255)
    number = models.CharField(_("Number"), max_length=255)
    response = models.TextField(_('Your entry'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = (
            ('export', 'Can export competition entries'),
        )
    
    @property
    def user_profile(self):
        try:
            return user.get_profile()
        except SiteProfileNotAvailable, e:
            return user

class WriteStoryEntry(models.Model):
    name = models.CharField(blank=False, max_length=255)
    email = models.EmailField(blank=True)
    cellphone = models.CharField(blank=True, max_length=100)
    website = models.CharField(blank=True, max_length=255)
    story = models.TextField(blank=False)
    terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.name

class Review(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, blank=True, null=True)
    review = models.TextField(blank=False)
    is_approved = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def review_object(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
    
    def name(self):
        story = ContentType.objects.get_for_model(Story)

        if self.content_type == story:
            return Story.objects.get(pk=self.object_id)
        else:
            return ""