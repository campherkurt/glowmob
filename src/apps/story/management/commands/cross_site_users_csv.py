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

def print_matching_profiles(writer, profile, matches):
    writer.writerow((profile.pk, profile, profile.mobile))
    writer.writerow(("","Matching MXit Profiles:"))
    writer.writerow(("","MXit Profile ID", "name", "mobile phone number"))
    for match in matches:
        writer.writerow(("", match.pk, match, match.mobile))
    

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
    help = 'Identify users with profiles on all the sites, identify duplicate profiles'
    
    def handle(self, **options):
        import csv, sys
        writer = csv.writer(sys.stdout)
        writer.writerow(("Mobi Profile ID", "name", "mobile phone number"))
        mobi_users = Profile.objects\
                        .exclude(mobile__isnull=True) \
                        .exclude(mobile__exact='') \
                        .filter(user_type=USER_TYPE_MOBI) \
                        .order_by('pk')
        
        exclude_list = []
        for profile in mobi_users.iterator():
            matches = find_matches(profile, USER_TYPE_MXIT, exclude_list)
            if matches:
                exclude_list.append(profile.pk)
                latest, older = find_latest(list(matches) + [profile])
                print_matching_profiles(writer, latest, older)
                
                
        
