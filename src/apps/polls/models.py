from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from apps.polls.constants import *
#from apps.story.models import Story

#==============================================================================
class Poll(models.Model):
    #story = models.ForeignKey(Story, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    question = models.CharField(_("Question"),max_length=200)
    #pub_date = models.DateTimeField(_('Date Published'))
    image = models.ImageField(upload_to='polls', blank=True, null=True)
    voted = models.ManyToManyField(User)
    display_on_homepage = models.BooleanField(_('Include on homepage'))

    class Meta:
        ordering = ['question']
        
    #--------------------------------------------------------------------------
    def __unicode__(self):
        return self.question
    
    #--------------------------------------------------------------------------
    def has_voted(self, User):
        
        return len(self.voted.filter(id=User.id)) > 0
    
    def generateResults(self):
        choices = self.choice_set.all()
    
        total_votes = sum(c.votes for c in choices)
        size_ratio = float(POLL_MAX_WIDTH) / 100.00 
        results = []
        for choice in choices:
            
            if choice.votes == 0:
                persentage = 0
    
            else:
                persentage = int((float(choice.votes) / float(total_votes)) * 100.00) 
                
            results.append({
                'choice': choice.choice,
                'votes': choice.votes,
                'persentage': persentage,
                'div_size': int(persentage * size_ratio)
                })
        
        return results
    
    def poll_results(self):
        results = self.generateResults()
        rows = ''
        for result in results:
            rows += '<tr> <td>%s</td><td>%s votes (%s %%)</td> </tr>' % (
                result['choice'],result['votes'], result['persentage'])
        
        return '<table id="collapse">%s</table>' % rows
    
    poll_results.allow_tags = True

#==============================================================================
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(_("Choice"),max_length=200)
    votes = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    #--------------------------------------------------------------------------
    class Meta:
        ordering = ('order', 'id')
    #--------------------------------------------------------------------------
    def __unicode__(self):
        return self.choice
