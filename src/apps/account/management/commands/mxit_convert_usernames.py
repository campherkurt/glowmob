from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import hashlib, base64
import traceback
from basic_profiles.models import USER_TYPE_MXIT

class Command(BaseCommand):
    help = 'Convert mxit usernames to md5 usernames'

    def handle(self, **options):
        users = User.objects.filter(profile__user_type=USER_TYPE_MXIT)
        count = users.count()
        print 'Start converting %s users...\n' % count

        for user in users:
            try:
                user.username = base64.b64encode(hashlib.md5(user.username).digest())
                user.save()
            except Exception, ex:
                print 'Exception:%s\n%s' % (str(ex), traceback.format_exc())
                count = count - 1
                pass

        print 'Done converting %s users\n' % count
