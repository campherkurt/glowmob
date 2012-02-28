from django.conf.urls.defaults import *



urlpatterns = patterns("",
    #url(r"^username_autocomplete/$", "pinax.apps.autocomplete_app.views.username_autocomplete_friends", name="profile_username_autocomplete"),
    url(r"^username_autocomplete/$", "pinax.apps.autocomplete_app.views.username_autocomplete_all", name="profile_username_autocomplete"),
    url(r"^$", "apps.basic_profiles.views.profiles", name="profile_list"),
    url(r"^profile/(?P<username>[\w\._-]+)/$", "apps.basic_profiles.views.profile", name="profile_detail"),
    url(r"^edit/$", "apps.basic_profiles.views.profile_edit", name="profile_edit"),
    url(r"^images/(on|off)/$", "apps.basic_profiles.views.toggle_images", name="toggle_images")
)