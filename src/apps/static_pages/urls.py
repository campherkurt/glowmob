from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^view/(?P<page_id>\d+)/$", "apps.static_pages.views.view", name="view_static_page"),
)
