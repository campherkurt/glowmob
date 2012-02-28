from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from apps.basic_profiles.models import Profile, USER_TYPE_MXIT, USER_TYPE_MOBI
from apps.story.models import Chapter
from apps.threadedcomments.models import ThreadedComment
from optparse import make_option
import sys, csv

class Command(BaseCommand):
    help = 'Print comment stats'
    option_list = BaseCommand.option_list + (
        make_option("--user-type",
            dest = "user_type",
            help = "What type of user to export data for"
        ),
    )
    
    
    def handle(self, **options):
        
        if not options['user_type']:
            sys.exit("Please provide what user type you're wanting to export " \
                        "with --user-type=[mxit|mobi]")
        
        if options.get('user_type') == 'mxit':
            self.do_mxit(**options)
        elif options.get('user_type') == 'mobi':
            self.do_mobi(**options)
    
    def do_mxit(self, **options):
        self.export(USER_TYPE_MXIT)
    
    def do_mobi(self, **options):
        self.export(USER_TYPE_MOBI)

    def export(self, user_type):
        content_type = ContentType.objects.get_for_model(Chapter)
        chapters = Chapter.objects.all()
        
        writer = csv.writer(sys.stdout)
        writer.writerow(('Story', 'Chapter', 'Total Comments'))
        
        for chapter in chapters:
            comments = ThreadedComment.objects.filter(
                        content_type=content_type, 
                        object_id=chapter.id,
                        user__profile__user_type=user_type)
            writer.writerow((
                chapter.story.title, 
                chapter.title, 
                comments.count()
            ))
