import traceback

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User

from apps.account.signals import user_logged_in
from basic_profiles.models import Profile, USER_TYPE_MOBI, USER_TYPE_MXIT
from urllib import unquote
import hashlib, base64

class TemplateRouting():

    def process_request(self, request):

        if request.META.has_key(settings.MXIT_HEADER):
            settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_MXIT + settings.TEMPLATE_DIRS_MOBI
            
            # Wrapping around a try block for now..
#            msisdn = unicode(request.META.get('HTTP_X_MXIT_ID_R', None), errors='ignore')
#            if msisdn:
#                try:
#                    try:
#                        profile = Profile.objects.filter(mobile=msisdn)
#                        user = profile[0].user
#                    except Exception, e:
#                        user = None
#
#                    if not user:
#                        user = User()
#                        user.username = msisdn[:30] # unique
#                        user.first_name = unquote(unicode(request.META['HTTP_X_MXIT_NICK'],errors='ignore'))[:30] # not unique
#                        user.set_password('mxit')
#                        user.save()
#
#                        profile = Profile.objects.get(user=user)
#                        profile.user = user
#                        profile.name = user.first_name
#                        profile.mobile = msisdn[:30]
#                        profile.user_type = USER_TYPE_MXIT
#                        profile.location = unicode(request.META['HTTP_X_MXIT_LOCATION'], errors='ignore')[:40]
#                        profile.save()
#
#                    if user:
#                        request.user = user
#                        request.user.mxit = True
#                except Exception, ex:
#                    print 'Exception:%s\n%s' % (str(ex), traceback.format_exc())
#                    pass

            msisdn = unicode(request.META.get('HTTP_X_MXIT_ID_R', None), errors='ignore')

            if msisdn:
                try:
                    try:
                        user = User.objects.filter(username=msisdn, profile__user_type=USER_TYPE_MXIT)[0]
                    except Exception, e:
                        user = None

                    unique_id = base64.b64encode(hashlib.md5(msisdn).digest())

                    if not user:
                        try:
                            user = User.objects.filter(username=unique_id, profile__user_type=USER_TYPE_MXIT)[0]
                        except Exception, e:
                            user = None

                    if not user:
                        user = User()
                        user.username = unique_id # unique
                        user.first_name = unquote(unicode(request.META['HTTP_X_MXIT_NICK'],errors='ignore'))[:30] # not unique
                        user.set_password('mxit')
                        user.save()

                        profile = Profile.objects.get(user=user)
                        profile.user = user
                        profile.name = user.first_name
                        profile.mobile = msisdn[:30]
                        profile.user_type = USER_TYPE_MXIT
                        profile.location = unicode(request.META['HTTP_X_MXIT_LOCATION'], errors='ignore')[:40]
                        profile.save()
                    print user
                    if user:
                        request.user = user
                        request.user.mxit = True
                except Exception, ex:
                    print 'Exception:%s\n%s' % (str(ex), traceback.format_exc())
                    pass
        else:
            settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS_MOBI + settings.TEMPLATE_DIRS_MXIT
