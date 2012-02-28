from django import template
from apps.static_pages.models import Page 

import apps.static_pages.constants
register = template.Library()

#------------------------------------------------------------------------------
@register.inclusion_tag("links.html")
def static_pages_links():
    pages = Page.objects.filter(type=apps.static_pages.constants.STATIC_PAGES_TYPE_GLOBAL)
    
    return {'pages': pages }