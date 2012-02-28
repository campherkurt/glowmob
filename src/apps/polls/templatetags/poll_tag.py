import random
import traceback

from django import template
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404

from apps.polls.constants import *
from apps.polls.models import Poll, Choice

import settings

register = template.Library()

#------------------------------------------------------------------------------
@register.inclusion_tag("poll2.html")
def show_poll(request, User, object):
    results = False

    if request.POST and request.POST.has_key('poll_id') and request.POST.has_key('choice'):
        
        poll = get_object_or_404(Poll, pk=request.POST['poll_id'])
        
        try:
            choice = poll.choice_set.get(pk=request.POST['choice'])
            choice.votes += 1
            choice.save()
        
            if User.is_authenticated():
                poll.voted.add(User)
                poll.save()
            
            else:
                if request.COOKIES.has_key('polls_voted') and request.COOKIES['polls_voted'] and\
                isinstance(request.COOKIES['polls_voted'], type([])):
                    if not poll.id in request.COOKIES['polls_voted']:
                    
                        tmp_cookie = request.COOKIES['polls_voted']
                        tmp_cookie.append(int(poll.id))
                    
                        # TODO: Add proper get and set methods instead of session space 
                        # Hackish way to add cookies. Using middleware to process the _request['cookies']
                        # and add it to the 'Real' cookies since access to the response object is needed.
                        request._cookies = {'polls_voted': tmp_cookie}
                else:
                
                    request._cookies = {'polls_voted':[int(poll.id),]}
        except Exception, e:
            print "Exception in poll", e
        
        results = _generateResults(poll)
        
    else:

        # TODO: Find out how polls should be displayed
        try:
            if object:
                if object.poll:
                    poll = object.poll
                else:
                    raise 'Object has no Poll'
            else:
                #poll = random.sample(Poll.objects.filter(story__isnull=True).all(),1)[0]
                poll = random.sample(Poll.objects.filter(display_on_homepage=True).all(),1)[0]
                
        except Exception, ex_msg:
            poll = None
            
        else:
            if poll.has_voted(User) or \
            (request.COOKIES.has_key('polls_voted') and str(int(poll.id)) in request.COOKIES['polls_voted']):
                results = _generateResults(poll)

    return {
        'poll': poll, 
        'results': results, 
        'max_width': POLL_MAX_WIDTH,
        'STATIC_URL': settings.STATIC_URL,
        }
    
#------------------------------------------------------------------------------
def _generateResults(poll):
    choices = poll.choice_set.all()

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
            'persentage': persentage,
            'div_size': int(persentage * size_ratio)
            })
    
    return results

@register.inclusion_tag("poll_mxit.html")
def show_poll_mxit(request, User, object):
    return show_poll(request, User, object)