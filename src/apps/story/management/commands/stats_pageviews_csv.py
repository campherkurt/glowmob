from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from apps.story.models import Story, Stat
from apps.basic_profiles.models import Profile, USER_TYPE_MOBI, USER_TYPE_MXIT
from django.contrib.auth.models import User
from datetime import date, timedelta
from optparse import make_option
import csv, sys

def per_day(query, field, start, stop=None):
    stop = stop or date.today()
    while start < stop:
        yield start, query.filter(**{
            "%s__lte" % field: start
        })
        start += timedelta(days=1)
    

class Command(BaseCommand):
    help = 'Print story stats'
    option_list = BaseCommand.option_list + (
        make_option("--user-type",
            dest = "user_type",
            help = "What type of user to export data for"
        ),
    )
    
    
    def handle(self, **options):
        
        if "user_type" not in options:
            sys.exit("Please provide what user type you're wanting to export with --user-type")
        
        self.launch_day = date(year=2010, month=8, day=22)
        
        if options.get('user_type') == 'mxit':
            self.do_mxit(**options)
        elif options.get('user_type') == 'mobi':
            self.do_mobi(**options)
    
    def export_csv(self, headers, qs, field, start):
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        for day, qs in per_day(qs, field, start):
            writer.writerow((day, qs.count()))
        
    
    def do_mxit(self, **options):
        self.generate_stats(USER_TYPE_MXIT)
    
    def do_mobi(self, **options):
        self.generate_stats(USER_TYPE_MOBI)
    
    def generate_stats(self, user_type):
        all_stories = Story.objects.all()
        story_type = ContentType.objects.get_for_model(Story)
        
        writer = csv.writer(sys.stdout)
        writer.writerow(('Story', 'Date', 'Pageviews'))
        
        for story in all_stories:
            stats = Stat.objects.filter(content_type=story_type, object_id=story.pk)
            mobi_stats = stats.filter(user__profile__user_type=user_type)
            for day, qs in per_day(mobi_stats, 'created', self.launch_day):
                writer.writerow((story.title, day, qs.count()))
        
        