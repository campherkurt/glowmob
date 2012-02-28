from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^$", "apps.share.views.index", name="site_share"),
)