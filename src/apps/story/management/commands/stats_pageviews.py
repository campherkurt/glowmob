from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Q

from apps.story.models import Story, Stat
from apps.basic_profiles.models import Profile, USER_TYPE_MOBI, USER_TYPE_MXIT
from datetime import datetime, timedelta

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
            'graph_title': 'Yoza Page views',
            'graph_category': 'Statistics',
            'graph_vlabel': 'Count',
            'graph_order': ' '.join([
                'total_pv',
                'total_mxit_pv',
                'total_mobi_pv',
                'week_pv',
                'week_mxit_pv',
                'week_mobi_pv',
                '24hr_pv',
                '24hr_mxit_pv',
                '24hr_mobi_pv',
            ]),
            'total_pv.label': 'Total',
            'total_mxit_pv.label': 'MXit',
            'total_mobi_pv.label': 'Mobi',
            'week_pv.label': 'Total last week',
            'week_mobi_pv.label': 'Total last week on Mobi',
            'week_mxit_pv.label': 'Total last week on MXit',
            '24hr_pv.label': 'Total last 24 hours',
            '24hr_mobi_pv.label': 'Total last 24 hours on Mobi',
            '24hr_mxit_pv.label': 'Total last 24 hours on MXit',
        })
    
    def handle_noargs(self, **options):
        
        # SET enable_seqscan = off
        from django.db import connection, transaction
        cursor = connection.cursor()
        
        cursor.execute("SET enable_seqscan = off")
        
        all_stories = Story.objects.all()
        all_story_ids = [story.pk for story in all_stories]
        story_content_type = ContentType.objects.get_for_model(Story)
        stats = Stat.objects.all()
        week_stats = stats.filter(created__gte=datetime.now() - timedelta(days=7))
        _24hr_stats = stats.filter(created__gte=datetime.now() - timedelta(days=1))
        
        self.format({
            'total_pv.value': stats.count(),
            'total_mxit_pv.value': stats.filter(user__profile__user_type=USER_TYPE_MXIT).count(),
            'total_mobi_pv.value': stats.filter(user__profile__user_type=USER_TYPE_MOBI).count(),
            'week_pv.value': week_stats.count(),
            'week_mxit_pv.value': week_stats.filter(user__profile__user_type=USER_TYPE_MXIT).count(),
            'week_mobi_pv.value': week_stats.filter(user__profile__user_type=USER_TYPE_MOBI).count(),
            '24hr_pv.value': _24hr_stats.count(),
            '24hr_mxit_pv.value': _24hr_stats.filter(user__profile__user_type=USER_TYPE_MXIT).count(),
            '24hr_mobi_pv.value': _24hr_stats.filter(user__profile__user_type=USER_TYPE_MOBI).count(),
        })
        
        cursor.execute("SET enable_seqscan = on")
        
