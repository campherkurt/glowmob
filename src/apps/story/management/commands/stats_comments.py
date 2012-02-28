from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from apps.basic_profiles.models import Profile, USER_TYPE_MXIT, USER_TYPE_MOBI
from apps.story.models import Chapter, Story
from apps.threadedcomments.models import ThreadedComment
from optparse import make_option
from datetime import datetime, timedelta
import sys, csv

class Command(BaseCommand):
    help = 'Print comment stats'
    option_list = BaseCommand.option_list + (
        make_option("--user-type",
            dest = "user_type",
            help = "What type of user to export data for"
        ),
    )
    
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
            'graph_title': 'Yoza Comments',
            'graph_category': 'Statistics',
            'graph_vlabel': 'Count',
            'graph_order': ' '.join([
                'total_chapter_comments',
                'total_chapter_mxit_comments',
                'total_chapter_mobi_comments',
                'week_chapter_comments',
                'week_chapter_mxit_comments',
                'week_chapter_mobi_comments',
                '24hr_chapter_comments',
                '24hr_chapter_mxit_comments',
                '24hr_chapter_mobi_comments',

                'total_story_comments',
                'total_story_mxit_comments',
                'total_story_mobi_comments',
                'week_story_comments',
                'week_story_mxit_comments',
                'week_story_mobi_comments',
                '24hr_story_comments',
                '24hr_story_mxit_comments',
                '24hr_story_mobi_comments',
            ]),
            
            'total_chapter_comments.label': 'Total on chapters',
            'total_chapter_mxit_comments.label': 'From MXit on chapters',
            'total_chapter_mobi_comments.label': 'From Mobi on chapters',
            'week_chapter_comments.label': 'Total last week on chapters',
            'week_chapter_mobi_comments.label': 'Total last week on Mobi on chapters',
            'week_chapter_mxit_comments.label': 'Total last week on MXit on chapters',
            '24hr_chapter_comments.label': 'Total last 24 hours on chapters',
            '24hr_chapter_mobi_comments.label': 'Total last 24 hours on Mobi on chapters',
            '24hr_chapter_mxit_comments.label': 'Total last 24 hours on MXit on chapters',
            
            'total_story_comments.label': 'Total on stories',
            'total_story_mxit_comments.label': 'MXit on stories',
            'total_story_mobi_comments.label': 'Mobi on stories',
            'week_story_comments.label': 'Total last week on stories',
            'week_story_mobi_comments.label': 'Total last week on Mobi on stories',
            'week_story_mxit_comments.label': 'Total last week on MXit on stories',
            '24hr_story_comments.label': 'Total last 24 hours on stories',
            '24hr_story_mobi_comments.label': 'Total last 24 hours on Mobi on stories',
            '24hr_story_mxit_comments.label': 'Total last 24 hours on MXit on stories',
        })
    
    def handle_noargs(self, **options):
        story_content_type = ContentType.objects.get_for_model(Story)
        chapter_content_type = ContentType.objects.get_for_model(Chapter)
        
        chapters = Chapter.objects.all()
        stories = Story.objects.all()
        
        
        def for_user_type(qs, user_type):
            return qs.filter(user__profile__user_type=user_type)
        
        def since(qs, **kwargs):
            return qs.filter(date_submitted__gte=datetime.now() - timedelta(**kwargs))
        
        chapter_comments = ThreadedComment.objects.filter(content_type=chapter_content_type)
        mxit_chapter_comments = for_user_type(chapter_comments, USER_TYPE_MXIT)
        mobi_chapter_comments = for_user_type(chapter_comments, USER_TYPE_MOBI)
        
        story_comments = ThreadedComment.objects.filter(content_type=story_content_type)
        mxit_story_comments = for_user_type(story_comments, USER_TYPE_MXIT)
        mobi_story_comments = for_user_type(story_comments, USER_TYPE_MOBI)
        
        self.format({
            'total_chapter_comments.value': chapter_comments.count(),
            'total_chapter_mxit_comments.value': mxit_chapter_comments.count(),
            'total_chapter_mobi_comments.value': mobi_chapter_comments.count(),
            'week_chapter_comments.value': since(chapter_comments, days=7).count(),
            'week_chapter_mxit_comments.value': since(mxit_chapter_comments, days=7).count(),
            'week_chapter_mobi_comments.value': since(mobi_chapter_comments, days=7).count(),
            '24hr_chapter_comments.value': since(chapter_comments, days=1).count(),
            '24hr_chapter_mxit_comments.value': since(mxit_chapter_comments, days=1).count(),
            '24hr_chapter_mobi_comments.value': since(mobi_chapter_comments, days=1).count(),

            'total_story_comments.value': story_comments.count(),
            'total_story_mxit_comments.value': mxit_story_comments.count(),
            'total_story_mobi_comments.value': mobi_story_comments.count(),
            'week_story_comments.value': since(story_comments, days=7).count(),
            'week_story_mxit_comments.value': since(mxit_story_comments, days=7).count(),
            'week_story_mobi_comments.value': since(mobi_story_comments, days=7).count(),
            '24hr_story_comments.value': since(story_comments, days=1).count(),
            '24hr_story_mxit_comments.value': since(mxit_story_comments, days=1).count(),
            '24hr_story_mobi_comments.value': since(mobi_story_comments, days=1).count(),
        })
        