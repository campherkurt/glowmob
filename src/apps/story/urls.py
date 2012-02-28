from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns("",
    url(r"^$", "apps.story.views.index", name="stories"),
    url(r"^write/$", "apps.story.views.write_story", name="write_story"),
    url(r"^genres/$", "apps.story.views.genres", name="genres"),
    url(r"^updates/$", "apps.story.views.updates", name="updates"),
    url(r"^browse/$", "apps.story.views.browse", name="browse"),
    url(r"^search/$", "apps.story.views.search", name="search"),
    url(r"^(?P<story_id>\d+)/$", "apps.story.views.story", name="story"),
    url(r"^(?P<story_id>\d+)/comment$", "apps.story.views.comment", name="comment"),
    url(r"^(?P<story_id>\d+)/review$", "apps.story.views.review", name="review"),
    url(r"^(?P<story_id>\d+)/vote$", "apps.story.views.vote", name="vote"),
    url(r"^chapter/(?P<chapter_id>\d+)/$", "apps.story.views.chapter", name="chapter"),
    url(r"^chapter/(?P<chapter_id>\d+)/vote$", "apps.story.views.chapter_vote", name="chapter_vote"),
    url(r"^chapter/(?P<chapter_id>\d+)/comment$", "apps.story.views.chapter_comment", name="chapter_comment"),
    url(r"^chapter/(?P<chapter_id>\d+)/share$", "apps.story.views.chapter_share", name="chapter_share"),
    url(r"^(?P<story_id>\d+)/share$", "apps.story.views.share", name="share"),
    url(r"^(?P<story_id>\d+)/downloads$", "apps.story.views.downloads", name="story_downloads"),
    url(r"^(?P<download_id>\d+)/download$", "apps.story.views.download", name="story_download"),
    url(r"^(?P<story_id>\d+)/competition$", "apps.story.views.competition", name="competition"),
    url(r"^(?P<story_id>\d+)/static_page/(?P<static_page_id>\d+)$", "apps.story.views.static_page", name="static_page"),
    url(r"^announcements/$", "apps.story.views.announcements", name="announcements"),
    url(r"^announcement/(?P<announcement_id>\d+)/$", "apps.story.views.announcement", name="announcement"),
    url(r"^report/(?P<story_id>\d+)/(?P<comment_id>\d+)/$", "apps.story.views.comment_report", name="comment_report"),
    url(r"^chapter_comment_report/(?P<chapter_id>\d+)/(?P<comment_id>\d+)/$", "apps.story.views.chapter_comment_report", name="chapter_comment_report"),
    
    #mxit
    url(r"^all/$", "apps.story.views.all_stories", name="all_stories"),
    url(r"^by_title/$", direct_to_template, {"template": "stories/stories_by_title.html",}, name="stories_by_title"),
    url(r"^by_title_range/$", "apps.story.views.by_title_range", name="stories_by_title_range"),
    url(r"^by_author/$", direct_to_template, {"template": "stories/stories_by_author.html",}, name="stories_by_author"),
    url(r"^by_author_range/$", "apps.story.views.by_author_range", name="stories_by_author_range"),
    url(r"^(?P<story_id>\d+)/chapters$", "apps.story.views.chapters", name="chapters"),
    url(r"^chapter/(?P<chapter_id>\d+)/page$", "apps.story.views.chapter_page", name="chapter_page"),
    url(r"^chapter/(?P<chapter_id>\d+)/comments$", "apps.story.views.chapter_comments", name="chapter_comments"),
    url(r"^(?P<story_id>\d+)/comments$", "apps.story.views.story_comments", name="story_comments"),
    url(r"^(?P<story_id>\d+)/reviews$", "apps.story.views.reviews", name="reviews"),
)