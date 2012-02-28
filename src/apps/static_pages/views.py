from apps.static_pages.models import Page

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def view(request, page_id):
    
    page = get_object_or_404(Page, pk=page_id)
    back = request.META.get('HTTP_REFERER', None)
    return render_to_response("static_pages/view.html", {
        "page": page,
        'back': back,
    }, context_instance=RequestContext(request))
