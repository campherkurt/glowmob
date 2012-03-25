from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from bookmarks.feeds import BookmarkFeed
from bookmarks.models import BookmarkInstance
from microblogging.feeds import TweetFeedAll, TweetFeedUser, TweetFeedUserWithFriends
from microblogging.models import Tweet
from swaps.models import Offer
from tagging.models import TaggedItem
from wiki.models import Article as WikiArticle

from pinax.apps.account.openid_consumer import PinaxConsumer
from pinax.apps.blog.feeds import BlogFeedAll, BlogFeedUser
from pinax.apps.blog.models import Post
from pinax.apps.photos.models import Image
from pinax.apps.topics.models import Topic
from pinax.apps.tribes.models import Tribe
from django.utils.datastructures import SortedDict

def new_sorted_dict(items):
    sorted_dict = SortedDict()
    for key, value in items:
        sorted_dict[key] = value
    return sorted_dict

handler500 = "pinax.views.server_error"

tweets_feed_dict = {"feed_dict": {
    "all": TweetFeedAll,
    "only": TweetFeedUser,
    "with_friends": TweetFeedUserWithFriends,
}}

blogs_feed_dict = {"feed_dict": {
    "all": BlogFeedAll,
    "only": BlogFeedUser,
}}

bookmarks_feed_dict = {"feed_dict": {"": BookmarkFeed }}


if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = "apps.account.views.signup"
else:
    signup_view = "pinax.apps.signup_codes.views.signup"


urlpatterns = patterns("",
#    url(r"^$", direct_to_template, {
#        "template": "homepage.html",
#    }, name="home"),
    url(r'^$', 'story.views.home', name="home"),
    
    url(r'^admin/graphs/(?P<category>.+)/$', 'story.views.admin_graph', name='view_graph'),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^account/signup/$", signup_view, name="acct_signup"),
    url(r"^competitions/(\d+)/$", 'story.views.site_competition', name="site_competition"),
    
    (r"^about/", include("about.urls")),
    (r"^account/", include("account.urls")),
    (r"^openid/(.*)", PinaxConsumer()),
    (r"^bbauth/", include("pinax.apps.bbauth.urls")),
    (r"^authsub/", include("pinax.apps.authsub.urls")),
    (r"^profiles/", include("apps.basic_profiles.urls")),
    (r"^blog/", include("pinax.apps.blog.urls")),
    (r"^invitations/", include("friends_app.urls")),
    (r"^notices/", include("notification.urls")),
    (r"^messages/", include("messages.urls")),
    (r"^announcements/", include("announcements.urls")),
    (r"^tweets/", include("microblogging.urls")),
    (r"^tribes/", include("pinax.apps.tribes.urls")),
    (r"^comments/", include("threadedcomments.urls")),
    (r"^robots.txt$", include("robots.urls")),
    (r"^i18n/", include("django.conf.urls.i18n")),
    (r"^bookmarks/", include("bookmarks.urls")),
    (r"^admin/", include(admin.site.urls)),
    (r"^photos/", include("pinax.apps.photos.urls")),
    (r"^avatar/", include("avatar.urls")),
    (r"^swaps/", include("swaps.urls")),
    (r"^flag/", include("flag.urls")),
    (r"^locations/", include("locations.urls")),
    (r"^genres/", include("genre.urls")),
    (r"^stories/", include("story.urls")),
    (r"^static_pages/", include("static_pages.urls")),
    (r"^contact/", include("contact.urls")),
    (r"^privacy/", include("privacy.urls")),
    (r"^terms/", include("terms.urls")),
    (r"^share/", include("share.urls")),
    (r"^feeds/tweets/(.*)/$", "django.contrib.syndication.views.feed", tweets_feed_dict),
    (r"^feeds/posts/(.*)/$", "django.contrib.syndication.views.feed", blogs_feed_dict),
    (r"^feeds/bookmarks/(.*)/?$", "django.contrib.syndication.views.feed", bookmarks_feed_dict),
)

# redirects
urlpatterns += patterns("",
    (r"^write/", redirect_to, {'url': '/stories/write/', 'permanent': False}),
    (r"^confessions/", redirect_to, {'url': '/stories/?series_id=4', 'permanent': False}),
    (r"^kontax/", redirect_to, {'url': '/stories/?series_id=1', 'permanent': False}),
    (r"^sisterz/", redirect_to, {'url': '/stories/?series_id=3', 'permanent': False}),
    (r"^streetskillz/", redirect_to, {'url': '/stories/?series_id=5', 'permanent': False}),
)

# rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

# exports
from apps.story.models import CompetitionEntry, Story, Chapter
from apps.threadedcomments.models import ThreadedComment
from apps.basic_profiles.models import Profile
#from export_csv.views import export_csv
#
#urlpatterns += patterns('',
#    url(r'^export/competition/entries\.csv$', export_csv,
#        {
#            'queryset': CompetitionEntry.objects.all(),
#            'not_available': 'n/a',
#            'require_permission': 'competitionentry.export',
#            'export_data':  new_sorted_dict([
#                ('competition.story','Story'),
#                ('competition.title','Competition'),
#                ('user','User'),
#                ('name','Name'),
#                ('number','Number'),
#                ('response','Response'),
#                ('created.date','Date Submitted'),
#                ('created.time','Time Submitted'),
#            ]),
#            'file_name': 'entries.csv',
#        }, "export_competition_entries"),
#    url(r'^export/story/comments\.csv$', export_csv,
#        {
#            'queryset': ThreadedComment.objects.all(),
#            'not_available': 'n/a',
#            'require_permission': 'threadedcomment.export',
#            'export_data':  new_sorted_dict([
#                ('content_type.name','Content Type'),
#                ('get_content_object_str','Content Object'),
#                ('user.id','User ID'),
#                ('user','User'),
#                ('date_submitted.date','Date Submitted'),
#                ('date_submitted.time','Time Submitted'),
#                ('comment','Comment'),
#                ('name','Name'),
#                ('cellphone','Telephone Number'),
#                ('get_status_display', 'Status'),
#            ]),
#            'file_name': 'comments.csv',
#        }, "export_story_comments"),
#    url(r'^export/user/profiles\.csv$', export_csv,
#        {
#            'queryset': Profile.objects.all(),
#            'not_available': 'n/a',
#            'require_permission': 'profile.export',
#            'export_data': new_sorted_dict([
#                ('user','Unique User ID'),
#                ('user.username','Unique User Name'),
#                ('user.email','Email Address'),
#                ('user.first_name','First Name'),
#                ('user.last_name','Last Name'),
#                ('mobile','Phone Number'),
#                ('user.threadedcomment_set.count','Comments Placed'),
#                ('get_user_type_display','User Type'),
#                ('user.date_joined','Date Joined'),
#            ]),
#            'file_name': 'profiles.csv'
#        }, "export_user_profiles"),
#    url(r'^export/story/chapters\.csv$', export_csv,
#        {
#            'queryset': Chapter.objects.all(),
#            'not_available': 'n/a',
#            'require_permission': 'story.export',
#            'export_data': new_sorted_dict([
#                ('story.title','Story'),
#                ('title','Chapter'),
#                ('comment_set.count','Number of comments'),
#                ('stat_set.count','Number of pageviews'),
#            ]),
#            'file_name': 'chapter.csv'
#        }, "export_story_chapter_stats"),
#    url(r'^export/stories\.csv$', export_csv, {
#        'queryset': Story.objects.all(),
#        'not_available': 'n/a',
#        'require_permission': 'story.export',
#        'export_data': new_sorted_dict([
#            ('title','Story'),
#            ('comment_set.count','Number of comments'),
#            ('stat_set.count','Number of pageviews'),
#        ]),
#        'file_name': 'stories.csv'
#    }, 'export_story_stats')
#)

# downloadable csv files
urlpatterns += patterns('',
    url(r'^export/stats/(?P<fn>[a-zA-Z\-\_]+)\.csv', 'apps.story.views.download_stats', {}, 'download_stats'),
)

#from apps.story.models import CompetitionEntry
#from apps.threadedcomments.models import ThreadedComment
#from export_csv.views import export_csv
#
#urlpatterns += patterns('',
#    url(r'^export/competition/entries\.csv$', export_csv,
#        {
#            'queryset': CompetitionEntry.objects.all(),
#            'not_available': 'n/a',
#            'require_permission': 'competitionentry.export',
#            'export_data':  {
#                'competition.story': 'Story',
#                'competition.title': 'Competition',
#                'user': 'User',
#                'name': 'Name',
#                'number': 'Number',
#                'response': 'Response',
#                'created.date': 'Date Submitted',
#                'created.time': 'Time Submitted',
#            },
#            'file_name': 'entries.csv',
#        }),
#    url(r'^export/story/comments\.csv$', export_csv,
#        {
#            'queryset': ThreadedComment.objects.all(),
#            'not_available': 'n/a',
#            'require_permission': 'threadedcomment.export',
#            'export_data':  {
#                'content_type.name': 'Content Type',
#                'get_content_object_str': 'Content Object',
#                'user.id': 'User ID',
#                'user': 'User',
#                'date_submitted.date': 'Date Submitted',
#                'date_submitted.time': 'Time Submitted',
#                'comment': 'Comment',
#                'name': 'Name',
#                'cellphone': 'Telephone Number',
#                'get_status_display': 'Status'
#            },
#            'file_name': 'comments.csv',
#        }),
#)



## @@@ for now, we'll use friends_app to glue this stuff together

friends_photos_kwargs = {
    "template_name": "photos/friends_photos.html",
    "friends_objects_function": lambda users: Image.objects.filter(is_public=True, member__in=users),
}

friends_blogs_kwargs = {
    "template_name": "blog/friends_posts.html",
    "friends_objects_function": lambda users: Post.objects.filter(author__in=users),
}

friends_tweets_kwargs = {
    "template_name": "microblogging/friends_tweets.html",
    "friends_objects_function": lambda users: Tweet.objects.filter(sender_id__in=[user.id for user in users], sender_type__name="user"),
}

friends_bookmarks_kwargs = {
    "template_name": "bookmarks/friends_bookmarks.html",
    "friends_objects_function": lambda users: Bookmark.objects.filter(saved_instances__user__in=users),
    "extra_context": {
        "user_bookmarks": lambda request: Bookmark.objects.filter(saved_instances__user=request.user),
    },
}

urlpatterns += patterns("",
    url(r"^photos/friends_photos/$", "friends_app.views.friends_objects", kwargs=friends_photos_kwargs, name="friends_photos"),
    url(r"^blog/friends_blogs/$", "friends_app.views.friends_objects", kwargs=friends_blogs_kwargs, name="friends_blogs"),
    url(r"^tweets/friends_tweets/$", "friends_app.views.friends_objects", kwargs=friends_tweets_kwargs, name="friends_tweets"),
    url(r"^bookmarks/friends_bookmarks/$", "friends_app.views.friends_objects", kwargs=friends_bookmarks_kwargs, name="friends_bookmarks"),
)

tagged_models = (
    dict(title="Blog Posts",
        query=lambda tag : TaggedItem.objects.get_by_model(Post, tag).filter(status=2),
        content_template="pinax_tagging_ext/blogs.html",
    ),
    dict(title="Bookmarks",
        query=lambda tag : TaggedItem.objects.get_by_model(BookmarkInstance, tag),
        content_template="pinax_tagging_ext/bookmarks.html",
    ),
    dict(title="Photos",
        query=lambda tag: TaggedItem.objects.get_by_model(Image, tag).filter(safetylevel=1),
        content_template="pinax_tagging_ext/photos.html",
    ),
    dict(title="Swap Offers",
        query=lambda tag : TaggedItem.objects.get_by_model(Offer, tag),
    ),
    dict(title="Topics",
        query=lambda tag: TaggedItem.objects.get_by_model(Topic, tag),
    ),
    dict(title="Tribes",
        query=lambda tag: TaggedItem.objects.get_by_model(Tribe, tag),
    ),
    dict(title="Wiki Articles",
        query=lambda tag: TaggedItem.objects.get_by_model(WikiArticle, tag),
    ),
)
tagging_ext_kwargs = {
    "tagged_models": tagged_models,
}

urlpatterns += patterns("",
    url(r"^tags/(?P<tag>.+)/(?P<model>.+)$", "tagging_ext.views.tag_by_model",
        kwargs=tagging_ext_kwargs, name="tagging_ext_tag_by_model"),
    url(r"^tags/(?P<tag>.+)/$", "tagging_ext.views.tag",
        kwargs=tagging_ext_kwargs, name="tagging_ext_tag"),
    url(r"^tags/$", "tagging_ext.views.index", name="tagging_ext_index"),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        (r"", include("staticfiles.urls")),
    )
