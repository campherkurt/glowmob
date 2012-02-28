from apps.genre.models import Genre
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    genres = Genre.objects.all()

    return render_to_response("genres/index.html", {
        "genres": genres
    }, context_instance=RequestContext(request))
    
