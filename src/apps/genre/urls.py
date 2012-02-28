from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^$", "apps.genre.views.index", name="genres"),
)