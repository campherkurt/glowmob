from django import template
register = template.Library()

from apps.story.forms import SearchForm

@register.inclusion_tag("search.html")
def search_tag(request):

    if request.method == "GET" and request.GET.has_key("search"):

        form = SearchForm(request.GET)
    
        if form.is_valid():
            pass
    else:
        form = SearchForm()
    return {
        'form': form
    }