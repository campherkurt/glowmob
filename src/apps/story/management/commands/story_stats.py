from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from apps.story.models import Story, Stat
from apps.basic_profiles.models import Profile
from django.contrib.auth.models import User
from datetime import date, timedelta
from optparse import make_option

USER_TYPE_MOBI = 1
USER_TYPE_MXIT = 2

def per_day(query, field, start, stop=None):
    stop = stop or date.today()
    while start < stop:
        yield start, query.filter(**{
            "%s__lte" % field: start
        })
        start += timedelta(days=1)
    

class Command(BaseCommand):
    help = 'Print story stats'
    
    def handle(self, config=None, **options):
        if config:
            self.handle_config(**options)
        else:
            return self.handle_noargs(**options)
    
    def format(self, dictionary):
        for k,v in dictionary.items():
            print "%s %s" % (str(k), str(v))
    
    def handle_config(self, **options):
        self.format({
            'graph_category': 'Statistics',
            'graph_vlabel': 'Uniques',
            'graph_order': 'total_uniques mxit_uniques mobi_uniques',
            'total_uniques.label': 'Total',
            'mxit_uniques.label': 'MXit',
            'mobi_uniques.label': 'Mobi'
        })
    
    def handle_noargs(self, **options):
        
        launch_day = date(year=2010, month=8, day=22)
        
        mxit_user_ids = [p.user_id for p in Profile.objects.raw(
                            """SELECT id, user_id FROM basic_profiles_profile 
                            WHERE user_type = %s""", [USER_TYPE_MXIT])]
        mobi_user_ids = [p.user_id for p in Profile.objects.raw(
                            """SELECT id, user_id FROM basic_profiles_profile
                            WHERE (user_type <> %s OR user_type IS NULL)""", [USER_TYPE_MXIT])]
        
        
        print "UNIQUES"
        print "=" * 50
        print "MXIT users: %s" % len(mxit_user_ids)
        for day, qs in per_day(User.objects.filter(pk__in=mxit_user_ids), 'date_joined', launch_day):
            print "\t%s: %s" % (day, qs.count())
        print 
        print "Mobi users: %s" % len(mobi_user_ids)
        for day, qs in per_day(User.objects.filter(pk__in=mobi_user_ids), 'date_joined', launch_day):
            print "\t%s: %s" % (day, qs.count())
        print
        all_stories = Story.objects.all()
        story_type = ContentType.objects.get_for_model(Story)
        
        print "PAGE VIEWS"
        print "=" * 50
        for story in all_stories:
            stats = Stat.objects.filter(content_type=story_type, object_id=story.pk)
            mxit_stats = stats.filter(user__in=mxit_user_ids)
            mobi_stats = stats.filter(user__in=mobi_user_ids)
            print "Story: %s" % story.title
            print "=" * 50
            print
            print "\tMXIT: %s (total)" % mxit_stats.count()
            print "\tBreak down per day"
            print "\t" + "-" * 50
            for day, qs in per_day(mxit_stats, 'created', launch_day):
                print "\t\t%s: %s" % (day, qs.count())
            print 
            print "\tMobi: %s (total)" % mobi_stats.count()
            print "\tBreak down per day"
            print "\t" + "-" * 50
            for day, qs in per_day(mobi_stats, 'created', launch_day):
                print "\t\t%s: %s" % (day, qs.count())
            print 
        