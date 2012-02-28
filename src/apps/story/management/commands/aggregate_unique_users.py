from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from apps.basic_profiles.models import Profile, USER_TYPE_MOBI, USER_TYPE_MXIT
from optparse import make_option

def find_matches(profile, user_type, exclude_list):
    qs = Profile.objects\
            .filter(mobile__endswith=profile.mobile[-9:]) \
            .filter(user_type=user_type) \
            .exclude(pk__in=exclude_list)
    return qs

def merge_profiles(profile, matches):
    print "Processing:", profile, "PK:", profile.pk, "mobile:", '%s' % profile.mobile
    for match in matches:
        print "\tMatch:", match, "PK:", match.pk, "mobile:", '%s' % match.mobile
        users_data = aggregate_data(match)
        for queryset in users_data:
            print "\t\tModel:", queryset.model.__name__, "COUNT: %s" % queryset.count()
            # queryset.update(user=profile)
        # match.is_active = False
        # match.save()
        
    

def find_latest(profiles):
    qs = Profile.objects.filter(pk__in=[p.pk for p in profiles]).order_by('pk')
    return qs[0], qs[1:]

def aggregate_data(profile):
    return [
        profile.user.competitionentry_set.all(),
        profile.user.poll_set.all(),
        profile.user.threadedcomment_set.all(),
        profile.user.vote_set.all()
    ]
    

class Command(BaseCommand):
    help = 'Identify unique users across the sites and aggregate them into a single User object instead of multiple across the sites'
    
    def handle(self, **options):
        mobi_users = Profile.objects\
                        .exclude(mobile__isnull=True) \
                        .exclude(mobile__exact='') \
                        .filter(
                            Q(user_type=USER_TYPE_MOBI) | Q(user_type__isnull=True)
                        ).order_by('pk')
        
        exclude_list = []
        for profile in mobi_users.iterator():
            matches = find_matches(profile, USER_TYPE_MXIT, exclude_list)
            if matches:
                exclude_list.append(profile.pk)
                latest, older = find_latest(list(matches) + [profile])
                merge_profiles(latest, older)
                
                
        
