from django.core.management.base import BaseCommand
from django.db.models import Q

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
            'graph_title': 'Yoza Uniques',
            'graph_category': 'Statistics',
            'graph_vlabel': 'Count',
            'graph_order': ' '.join([
                'total_uniques',
                'total_mxit_uniques',
                'total_mobi_uniques',
                '24hr_uniques',
                '24hr_mxit_uniques',
                '24hr_mobi_uniques',
            ]),
            'total_uniques.label': 'Total',
            'total_mxit_uniques.label': 'MXit',
            'total_mobi_uniques.label': 'Mobi',
            '24hr_uniques.label': 'In the last 24 hours',
            '24hr_mxit_uniques.label': 'In the last 24 hours on MXit',
            '24hr_mobi_uniques.label': 'In the last 24 hours on Mobi',
        })
    
    def handle_noargs(self, **options):
        profiles = Profile.objects.all()
        mxit_profiles = profiles.filter(user_type=USER_TYPE_MXIT)
        mobi_profiles = profiles.filter(Q(user_type=USER_TYPE_MOBI) | Q(user_type__isnull=True))
        
        def last_24_hours(query):
            return query.filter(user__date_joined__gte=datetime.now() - timedelta(days=1))
        
        self.format({
            'total_uniques.value': profiles.count(),
            'total_mxit_uniques.value': mxit_profiles.count(),
            'total_mobi_uniques.value': mobi_profiles.count(),
            '24hr_uniques.value': last_24_hours(profiles).count(),
            '24hr_mobi_uniques.value': last_24_hours(mobi_profiles).count(),
            '24hr_mxit_uniques.value': last_24_hours(mxit_profiles).count(),
        })