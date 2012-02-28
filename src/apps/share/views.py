from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site

def index(request):
    current_site = Site.objects.get_current()

    return render_to_response("share/index.html", {
        "domain": current_site.domain
    }, context_instance=RequestContext(request))