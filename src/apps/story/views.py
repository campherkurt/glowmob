from apps.story.models import Story, Genre, Chapter, Stat, Download, Competition, CompetitionEntry, Announcement, Language, Series, Review
from apps.static_pages.models import Page
import os.path
from datetime import datetime
from sorl.thumbnail.base import Thumbnail
from sorl.thumbnail.main import build_thumbnail_name

import threadedcomments.models
import general.models
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.story.forms import SearchForm, CommentForm, CompetitionForm, WriteStoryEntryForm, ReviewForm
from django.contrib.contenttypes.models import ContentType
from threadedcomments.models import ThreadedComment

from voting.models import Vote
from voting.views import VOTE_DIRECTIONS
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.sites.models import Site
from django.db.models import Count
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.vary import vary_on_headers
from django.contrib.admin.views.decorators import staff_member_required

from settings import MEDIA_ROOT, MXIT_HEADER, CACHE_SECONDS, CACHE_VARY_ON_HEADERS, PROJECT_ROOT
from apps.story.models import Announcement
from apps.story.utils import cache_page_with_dynamic_key
from apps.basic_profiles.models import Profile

import math

def generate_cache_key_from_request(request):
    if request.META.has_key(MXIT_HEADER):
        site = 'mxit'
        username = ''
    else:
        site = 'mobi'
        if request.user.is_anonymous():
            username = ''
        else:
            username = request.user.username
    
    # cache for 60 seconds with the given key
    return (CACHE_SECONDS, "%(site)s://%(username)s@%(path)s?%(qs)s" % {
        'site': site,
        'username': username,
        'path': request.path,
        'qs': request.META.get('QUERY_STRING','')
    })

def has_permission_to_review(request, story):
    if request.user.is_authenticated() and story.is_finished:
        chapters = Chapter.objects.filter(story=story).filter(publish_date__lte=datetime.now())
        chapter_count = chapters.count()
        #print chapter_count
        ids = chapters.values_list('id', flat=True)
        content_type = ContentType.objects.get_for_model(Chapter)
        stat_count = Stat.objects.filter(user=request.user, content_type=content_type, object_id__in=ids).values('object_id').distinct().count()
        print stat_count
        if stat_count == chapter_count:
            return True

    return False
    
#====================================== MXIT ===================================
@vary_on_headers(*CACHE_VARY_ON_HEADERS)
@cache_page_with_dynamic_key(generate_cache_key_from_request)
def home(request):
    
    active_filter = "new"
    
    try:
        profile = request.user.profile_set.latest('pk')
    except ObjectDoesNotExist, e:
        profile = None
    except AttributeError, e: # anonymous user
        profile = None
    
    announcements = Announcement.objects.order_by("-created")[:5]
    competitions = Competition.visible.filter(story__isnull=True)
    
    features = general.models.Featured.objects.order_by('-created')[:5]
    
    content_type = ContentType.objects.get_for_model(Story)

    stories = Story.public
    stories = stories.exclude(type='classic')
    stories = stories.filter(display_on_homepage=1)

    if request.GET.has_key("popular"):
        stories = stories.extra(
            select = {
                'stat_count': '(select count(*) FROM story_stat where content_type_id = ' + str(content_type.id) + ' and object_id = story_story.id)'
            },
        ).order_by("-stat_count")
        
        active_filter = "popular"
    else:
        stories = stories.order_by("-created")

    stories = stories[:5]

    return render_to_response("stories/home.html", {
        "stories": stories,
        "announcements": announcements,
        "active_filter": active_filter,
        "competitions": competitions,
        "story": None,
        "features": features,
        "profile": profile,
    }, context_instance=RequestContext(request))
    
def updates(request):
    announcements = Announcement.objects.all().order_by('-created')

    return render_to_response("stories/updates.html", {
        "announcements": announcements
    }, context_instance=RequestContext(request))

def by_title_range(request):
    stories = Story.public
    
    if request.GET.has_key("r"):
        stories = stories.filter(title__iregex=r'^[' + request.GET['r'] + ']').order_by("title")
    else:
        stories = stories.all()

    return render_to_response("stories/stories_by_title_range.html", {
        "stories": stories,
        "r": request.GET['r']
    }, context_instance=RequestContext(request))

def by_author_range(request):
    stories = Story.public

    if request.GET.has_key("r"):
        stories = stories.filter(author__iregex=r'^[' + request.GET['r'] + ']').order_by("author")
    else:
        stories = stories.all()

    return render_to_response("stories/stories_by_author_range.html", {
        "stories": stories,
        "r": request.GET['r']
    }, context_instance=RequestContext(request))
    
#====================================== MXIT ===================================
@vary_on_headers(*CACHE_VARY_ON_HEADERS)
@cache_page_with_dynamic_key(generate_cache_key_from_request) # 1 minute
def index(request):
    stories = Story.public
    genre = None
    language = None
    series = None
    
    try:
        profile = request.user.profile_set.latest('pk')
    except ObjectDoesNotExist, e:
        profile = None
    except AttributeError, e:
        profile = None
    
    if request.method == "GET":
        if request.GET.get("genre_id"):
            genre_id =request.GET["genre_id"]
            genre = Genre.objects.get(id=genre_id)
            stories = stories.filter(genre=genre_id)
    
        if request.GET.get("language_id"):
            language_id =request.GET["language_id"]
            language = Language.objects.get(id=language_id)
            stories = stories.filter(language=language)

        if request.GET.get("series_id"):
            series_id =request.GET["series_id"]
            series = Series.objects.get(id=series_id)
            stories = stories.filter(series=series)
            
    if request.method == "GET":
        if request.GET.has_key("type"):
            stories = stories.filter(type=request.GET["type"])

    stories = stories.all()

    return render_to_response("stories/index.html", {
        "stories": stories,
        "genre": genre,
        "language": language,
        "series": series,
        "profile": profile,
    }, context_instance=RequestContext(request))

@vary_on_headers(*CACHE_VARY_ON_HEADERS)
@cache_page_with_dynamic_key(generate_cache_key_from_request) # 1 minute
def genres(request):
    genres = Genre.objects.all()

    return render_to_response("stories/genres.html", {
        "genres": genres
    }, context_instance=RequestContext(request))
    
@vary_on_headers(*CACHE_VARY_ON_HEADERS)
@cache_page_with_dynamic_key(generate_cache_key_from_request) # 1 minute
def browse(request):
    active_filter = "new"
    
    try:
        profile = request.user.profile_set.latest('pk')
    except ObjectDoesNotExist, e:
        profile = None
    except AttributeError, e: # anonymous user
        profile = None
    
    if request.method == "POST" and not request.POST.has_key("poll_id"):
        form = SearchForm(request.POST)

        if form.is_valid():
            pass
    else:
        form = SearchForm()
        
    genres = Genre.objects.all()

    languages = Language.objects.all()

    content_type = ContentType.objects.get_for_model(Story)
    
    if request.GET.has_key("popular"):
        stories = Story.objects.extra(
            select = {
                'stat_count': '(select count(*) FROM story_stat where content_type_id = ' + str(content_type.id) + ' and object_id = story_story.id)'
            },
        ).order_by("-stat_count")[:3]
        active_filter = "popular"
    else:
        stories = Story.public.order_by("-created")

    stories = stories[:3]

    return render_to_response("stories/browse.html", {
        "form": form,
        "genres": genres,
        "languages": languages,
        "stories": stories,
        "active_filter": active_filter,
        "profile": profile,
    }, context_instance=RequestContext(request))

def search(request):
    
    stories = Story.public
    
    if request.method == "GET":
        if request.GET.has_key("search_by"):
            search = request.GET["search"]
            search_by = int(request.GET["search_by"])

            if search_by == 1:
                stories = stories.filter(title__icontains=search)
            if search_by == 2:
                stories = stories.filter(author__icontains=search)
            if search_by == 3:
                stories = stories.filter(genre__name__icontains=search)

    stories = stories.all()
    
    return render_to_response("stories/search.html", {
        "stories": stories,
        "search": search,
        "count": stories.count(),
    }, context_instance=RequestContext(request))

@vary_on_headers(*CACHE_VARY_ON_HEADERS)
@cache_page_with_dynamic_key(generate_cache_key_from_request) # 1 minute
def story(request, story_id):
#    if not request.META.has_key(MXIT_HEADER):
#        if not request.user.is_authenticated():
#            return HttpResponseRedirect("/account/login/")
    
    story = Story.public.get(id=story_id)
    
    chapters = Chapter.objects.filter(story=story).filter(publish_date__lte=datetime.now()).order_by('order','created','id')
    
    chapter = chapters[:1]
    try:
        chapter = chapter[0]
    except:
        chapter = None
    
    content_type = ContentType.objects.get_for_model(Story)
    
    comments = ThreadedComment.objects.filter(
        content_type=content_type, 
        object_id=story.id,
        ).exclude(status=threadedcomments.models.STATUS_MODERATION)

    comments = comments.order_by("-date_submitted")

    
    if request.user.is_authenticated():
        stat = Stat(content_type=content_type, object_id=story.id, user=request.user)
    else:
        stat = Stat(content_type=content_type, object_id=story.id)
        
    stat.save()

    from apps.story.models import Announcement

    announcements = Announcement.objects.filter(story=story).order_by("-created")[:5]
    
    try:
        back = request.META.get('HTTP_REFERER', None)
    except:
        back = None

    competition = Competition.visible.filter(story=story).order_by("-created")[:1]
    if len(competition)> 0:
        competition = competition[0]
    #print '\\n\n\n\n\n\n\n\nComp %s\n\n\n\n\n' % competition[0].title
    pages = Chapter.objects.filter(story=story)[:1]
    
    static_pages = story.page_set.all()

    reviews = Review.objects.filter(
        content_type=content_type,
        object_id=story.id,
        is_approved=True
    )
    review_count = reviews.count()

    try:
        page = int(request.GET['page'])
    except:
        page = 1
    
    data = {
        "story": story,
        "chapters": chapters,
        "comments": comments,
        "chapter": chapter,
        "announcements": announcements,
        "competition": competition,
        #"page": page,
        'static_pages': static_pages,
        'review_count': review_count,
        'page': page,
        "back": back
    }

    try:
        page = int(request.GET['review_page'])
    except:
        page = 1

    data["review_page"] = page

    data["has_review_permission"] = False

    if has_permission_to_review(request, story):
        data["has_review_permission"] = True

    if review_count > 0:
        limit = 6
        page_count = int(math.ceil(review_count/float(limit)))

        reviews = reviews[(page - 1) * limit: page * limit]

        prev = False
        prev_page = 1
        next = False
        next_page = page_count

        if page > 1:
            prev = True
            prev_page = page - 1

        if page < page_count:
            next = True
            next_page = page + 1

        if page * limit > review_count:
            to = review_count
        else:
            to = page * limit

        data["start"] = ((page - 1) * limit)

        data['reviews'] = reviews

        data["indicator"] = "%s - %s of %s" % ((((page - 1) * limit) + 1), to, review_count)
        data["prev"] = prev
        data["prev_page"] = prev_page
        data["next"] = next
        data["next_page"] = next_page

    return render_to_response("stories/story.html", data, context_instance=RequestContext(request))

@vary_on_headers()
@cache_page_with_dynamic_key(generate_cache_key_from_request) # 1 minute
def chapter(request, chapter_id):
        
    chapter = get_object_or_404(Chapter, id=chapter_id)
    content_type = ContentType.objects.get_for_model(Chapter)
    
    if request.user.is_authenticated():
        profile = request.user.profile_set.latest('pk')
        profile.last_story = chapter.story
        profile.last_chapter = chapter
        profile.save()
        stat = Stat(content_type=content_type, object_id=chapter.pk, user=request.user)
    else:
        stat = Stat(content_type=content_type, object_id=chapter.pk)
    stat.save()
    

    comments = ThreadedComment.objects.filter(
        content_type=content_type,
        object_id=chapter.id
        ).exclude(status=threadedcomments.models.STATUS_MODERATION)

    comments = comments.order_by("-date_submitted")

    variables = {
        "chapter": chapter,
        "comments": comments,
    }
    
    if request.GET.has_key("p"):
        p = int(request.GET["p"] or 1)
        if p == 1:
            start = 0
        else:
            start = p - 2
        chapters = Chapter.objects.filter(story=chapter.story).filter(publish_date__lte=datetime.now()).order_by('order','created','id')
        total_count = chapters.count()
        chapters = chapters[start : p + 1]

        if p > 1:
            variables["prev_chapter"] = Chapter.objects.get(id=chapters[0].id)
            
        if p + 1 <= total_count:
            if chapters.count() == 3:
                variables["next_chapter"] = Chapter.objects.get(id=chapters[2].id)
            elif chapters.count() == 2:
                variables["next_chapter"] = Chapter.objects.get(id=chapters[1].id)
            
        variables["next_page"] = p + 1
        variables["prev_page"] = p - 1
        variables["p"] = p

    return render_to_response("stories/chapter.html", variables, context_instance=RequestContext(request))

def comment(request, story_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    story = Story.public.get(id=story_id)
    content_type = ContentType.objects.get_for_model(Story)

    form = CommentForm()

    if not request.META.has_key(MXIT_HEADER):
        del form.fields["name"]
        del form.fields["cellphone"]

#    if request.method == "GET" and request.GET.has_key("error"):
#        form = CommentForm(request.GET)
#        if form.is_valid():
#            pass

    try:
        back = request.GET["back"]
    except:
        back = None
        
    return render_to_response("stories/comment.html", {
        "story": story,
        "form": form,
        "content_type": content_type,
        "back": back
    }, context_instance=RequestContext(request))

def review(request, story_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('story', kwargs={'story_id': story_id}))

    story = Story.public.get(id=story_id)
    
    if not has_permission_to_review(request, story):
        return HttpResponseRedirect(reverse('story', kwargs={'story_id': story_id}))
    
    content_type = ContentType.objects.get_for_model(Story)

    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save(request.user, story, content_type)
            messages.add_message(request, messages.SUCCESS, "Your review has been posted successfully.")
            return HttpResponseRedirect(request.POST["next"])
    try:
        back = request.GET["back"]
    except:
        back = None

    return render_to_response("stories/review.html", {
        "story": story,
        "form": form,
        "content_type": content_type,
        "back": back
    }, context_instance=RequestContext(request))
    
def chapter_comment(request, chapter_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    chapter = get_object_or_404(Chapter, id=chapter_id)
    content_type = ContentType.objects.get_for_model(Chapter)

    form = CommentForm()

    if not request.META.has_key(MXIT_HEADER):
        del form.fields["name"]
        del form.fields["cellphone"]

    if request.method == "GET" and request.GET.has_key("error"):
        form = CommentForm(request.GET)
        if form.is_valid():
            pass

    p = None

    if request.method == "GET" and request.GET.has_key("p"):
        p = request.GET["p"]
    
    return render_to_response("stories/chapter_comment.html", {
        "chapter": chapter,
        "form": form,
        "content_type": content_type,
        "p": p,
    }, context_instance=RequestContext(request))

def vote(request, story_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    story = Story.public.get(id=story_id)
    content_type = ContentType.objects.get_for_model(Story)

    if request.method == "GET":
        if request.GET.has_key("choice"):
            if request.GET["choice"] == "yes":
                vote = dict(VOTE_DIRECTIONS)["up"]
                Vote.objects.record_vote(story, request.user, vote)

                messages.add_message(request, messages.SUCCESS, "Your vote has been recorded successfully.")

            return HttpResponseRedirect(request.GET["next"])

    return render_to_response("stories/vote.html", {
        "story": story,
        "content_type": content_type,
    }, context_instance=RequestContext(request))

def chapter_vote(request, chapter_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    chapter = get_object_or_404(Chapter, id=chapter_id)
    content_type = ContentType.objects.get_for_model(Chapter)
    

    if request.method == "GET":
        if request.GET.has_key("choice"):
            if request.GET["choice"] == "yes":
                vote = dict(VOTE_DIRECTIONS)["up"]
                Vote.objects.record_vote(chapter, request.user, vote)

                messages.add_message(request, messages.SUCCESS, "Your vote has been recorded successfully.")

            return HttpResponseRedirect(request.GET["next"])

    p = request.GET["p"]
    
    return render_to_response("stories/chapter_vote.html", {
        "chapter": chapter,
        "content_type": content_type,
        "p": p
    }, context_instance=RequestContext(request))

def share(request, story_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    story = Story.public.get(id=story_id)

    current_site = Site.objects.get_current()

    return render_to_response("stories/share.html", {
        "story": story,
        "domain": current_site.domain
    }, context_instance=RequestContext(request))

def static_page(request, story_id, static_page_id):
    page = Page.objects.filter(pk=static_page_id)
    story = Story.public.get(id=story_id)
    back = request.META.get('HTTP_REFERER', None)
    if len(page) > 0:
        page = page[0]
    else:
        page = None
        
    return render_to_response("stories/static_page.html", {
        "story": story,
        "page": page,
        'back': back
    }, context_instance=RequestContext(request))

def chapter_share(request, chapter_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")

    p = None

    if request.method == "GET" and request.GET.has_key("p"):
        p = request.GET["p"]

    chapter = get_object_or_404(Chapter, id=chapter_id)

    current_site = Site.objects.get_current()

    return render_to_response("stories/chapter_share.html", {
        "chapter": chapter,
        "domain": current_site.domain,
        "p": p
    }, context_instance=RequestContext(request))

def downloads(request, story_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    story = Story.public.get(id=story_id)

    downloads = Download.objects.filter(story=story)

    wallpapers = Download.objects.filter(story=story).filter(type='image')
    
    ringtones = Download.objects.filter(story=story).filter(type='ringtone')

    return render_to_response("stories/downloads.html", {
        "story": story,
        "downloads": downloads,
        "wallpapers": wallpapers,
        "ringtones": ringtones
    }, context_instance=RequestContext(request))

def download(request, download_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    download = Download.objects.get(id=download_id)
    filename = os.path.join(MEDIA_ROOT, str(download.download))
    
    if download.type == 'image' and 'HTTP_UA_PIXELS' in request.META:
        size = tuple(int(v) for v in request.META.get('HTTP_UA_PIXELS', '').split("x"))
        outfile = build_thumbnail_name(filename, size)
        thumbnail = Thumbnail(filename, size, dest=outfile)
        wrapper = FileWrapper(file(thumbnail.dest,"rb"))
    else:
        wrapper = FileWrapper(file(filename,"rb"))
    
    response = HttpResponse(wrapper, mimetype='application/force-download')
    filename = str(download.download).split("/")
    filename = filename[len(filename) - 1]

    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    
    return response

def competition(request, story_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
        
    story = Story.public.get(id=story_id)
    try:
        competition = Competition.visible.filter(story=story).latest("created")
    except Competition.DoesNotExist:
        raise Http404
    
    form = CompetitionForm()

#    if not request.META.has_key(MXIT_HEADER):
#        del form.fields["name"]
#        del form.fields["number"]
        
    back = None

    try:
        back = request.GET["back"]
    except:
        back = None
        
    if request.method == "POST":
        form = CompetitionForm(request.POST)

#        if not request.META.has_key(MXIT_HEADER):
#            del form.fields["name"]
#            del form.fields["number"]
        
        back = request.POST["back"]

        if form.is_valid():
            entry = CompetitionEntry(
                competition=competition,
                response=request.POST["response"]
            )

            if request.user.is_authenticated():
                entry.user = request.user

            #if request.META.has_key(MXIT_HEADER):
            entry.name = request.POST["name"]
            entry.number = request.POST["number"]
                
            entry.save()

            messages.add_message(request, messages.SUCCESS, "You entered the competition successfully.")

            return HttpResponseRedirect(request.POST["next"])

    return render_to_response("stories/competition.html", {
        "competition": competition,
        "form": form,
        "back": back,
    }, context_instance=RequestContext(request))

@vary_on_headers(*CACHE_VARY_ON_HEADERS)
@cache_page_with_dynamic_key(generate_cache_key_from_request)
def site_competition(request, competition_id):
    if not request.META.has_key(MXIT_HEADER):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/account/login/")
    
    try:
        competition = Competition.visible.get(pk=competition_id)
    except Competition.DoesNotExist:
        raise Http404
    
    form = CompetitionForm()
    back = request.GET.get("back")
    
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        back = request.POST.get("back")
        
        if form.is_valid():
            entry = CompetitionEntry(
                competition=competition,
                response=request.POST["response"]
            )
            
            if request.user.is_authenticated():
                entry.user = request.user
            
            entry.name = request.POST["name"]
            entry.number = request.POST["number"]
            entry.save()
            
            messages.add_message(request, messages.SUCCESS, "You entered the competition successfully.")
            
            return HttpResponseRedirect(request.POST["next"])
    
    return render_to_response("stories/site_competition.html", {
        "competition": competition,
        "form": form,
        "back": back,
    }, context_instance=RequestContext(request))



def announcements(request):
    announcements = Announcement.objects.all()
    return render_to_response("stories/announcements.html", {
        "announcements": announcements,
    }, context_instance=RequestContext(request))

def announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    return render_to_response("stories/announcement.html", {
        "announcement": announcement,
    }, context_instance=RequestContext(request))

def all_stories(request):
    languages = Language.objects.all().order_by("language")
    genres = Genre.objects.all().order_by("name")
    
    return render_to_response("stories/all_stories.html", {
        "languages": languages,
        "genres": genres
    }, context_instance=RequestContext(request))

def chapters(request, story_id):
    story = Story.public.get(id=story_id)

    chapters = Chapter.objects.filter(story=story).filter(publish_date__lte=datetime.now()).order_by('order','created','id')

    return render_to_response("stories/chapters.html", {
        "story": story,
        "chapters": chapters
    }, context_instance=RequestContext(request))

def chapter_page(request, chapter_id):
    p = None
    
    if request.GET.has_key("p"):
        p = request.GET["p"]

    chapter = get_object_or_404(Chapter, id=chapter_id)

    return render_to_response("stories/chapter_page.html", {
        "chapter": chapter,
        "p": p
    }, context_instance=RequestContext(request))

def chapter_comments(request, chapter_id):
    p = None
    back = None
    
    if request.GET.has_key("p"):
        p = request.GET["p"]

    if request.GET.has_key("back"):
        back = request.GET["back"]
        
    chapter = get_object_or_404(Chapter, id=chapter_id)

    content_type = ContentType.objects.get_for_model(Chapter)

    comments = ThreadedComment.objects.filter(
        content_type=content_type,
        object_id=chapter.id
        ).exclude(status=threadedcomments.models.STATUS_MODERATION)

    comments = comments.order_by("-date_submitted")

    return render_to_response("stories/chapter_comments.html", {
        "comments": comments,
        "chapter": chapter,
        "p": p,
        "back": back
    }, context_instance=RequestContext(request))

def story_comments(request, story_id):
    story = Story.public.get(id=story_id)

    content_type = ContentType.objects.get_for_model(Story)

    comments = ThreadedComment.objects.filter(
        content_type=content_type,
        object_id=story.id,
        ).exclude(status=threadedcomments.models.STATUS_MODERATION)

    comments = comments.order_by("-date_submitted")

    return render_to_response("stories/story_comments.html", {
        "comments": comments,
        "story": story
    }, context_instance=RequestContext(request))

def reviews(request, story_id):
    story = Story.public.get(id=story_id)

    if not has_permission_to_review(request, story):
        return HttpResponseRedirect(reverse('story', kwargs={'story_id': story_id}))
    
    content_type = ContentType.objects.get_for_model(Story)
    
    reviews = Review.objects.filter(
        content_type=content_type,
        object_id=story.id,
        is_approved=True
    )

    return render_to_response("stories/reviews.html", {
        "reviews": reviews,
        "story": story
    }, context_instance=RequestContext(request))

def write_story(request):
    if request.POST:
        form = WriteStoryEntryForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = WriteStoryEntryForm()
        success = False
    return render_to_response("stories/write_story.html", {
        "form": form
    }, context_instance=RequestContext(request))

def comment_report(request, story_id, comment_id):
    story = get_object_or_404(Story, id=int(story_id))
    tc = get_object_or_404(ThreadedComment, id=int(comment_id))

    return render_to_response("stories/comment_report.html", {
        "story": story,
        "tc": tc
    }, context_instance=RequestContext(request))

def chapter_comment_report(request, chapter_id, comment_id):
    chapter = get_object_or_404(Chapter, id=int(chapter_id))
    tc = get_object_or_404(ThreadedComment, id=int(comment_id))

    return render_to_response("stories/chapter_comment_report.html", {
        "chapter": chapter,
        "tc": tc
    }, context_instance=RequestContext(request))

@staff_member_required
def admin_graph(request, category):
    return render_to_response(
        "admin/graph.html",
        { "category": category },
        RequestContext(request)
    )

@staff_member_required
def download_stats(request, fn):
    file_path = os.path.join(PROJECT_ROOT,"stats","%s.csv" % fn)
    wrapper = FileWrapper(file(file_path,"rb"))
    response = HttpResponse(wrapper, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % fn
    return response