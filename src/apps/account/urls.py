from django.conf.urls.defaults import *

from apps.account.forms import SignupForm



urlpatterns = patterns("",
    url(r"^email/$", "apps.account.views.email", name="acct_email"),
    url(r"^signup/$", "apps.account.views.signup", name="acct_signup"),
    url(r"^login/$", "account.views.login", name="acct_login"),
    url(r"^login/openid/$", "apps.account.views.login", {"associate_openid": True},
        name="acct_login_openid"),
    url(r"^password_change/$", "apps.account.views.password_change", name="acct_passwd"),
    url(r"^password_set/$", "apps.account.views.password_set", name="acct_passwd_set"),
    url(r"^password_delete/$", "apps.account.views.password_delete", name="acct_passwd_delete"),
    url(r"^password_delete/done/$", "django.views.generic.simple.direct_to_template", {
        "template": "account/password_delete_done.html",
    }, name="acct_passwd_delete_done"),
    url(r"^timezone/$", "apps.account.views.timezone_change", name="acct_timezone_change"),
    url(r"^other_services/$", "apps.account.views.other_services", name="acct_other_services"),
    url(r"^other_services/remove/$", "apps.account.views.other_services_remove", name="acct_other_services_remove"),
    
    url(r"^language/$", "apps.account.views.language_change", name="acct_language_change"),
    url(r"^logout/$", "django.contrib.auth.views.logout", {"template_name": "account/logout.html"}, name="acct_logout"),
    
    url(r"^confirm_email/(\w+)/$", "emailconfirmation.views.confirm_email", name="acct_confirm_email"),
    
    # password reset
    url(r"^password_reset/$", "apps.account.views.password_reset", name="acct_passwd_reset"),
    url(r"^password_reset/done/$", "apps.account.views.password_reset_done", name="acct_passwd_reset_done"),
    url(r"^password_reset_key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", "apps.account.views.password_reset_from_key", name="acct_passwd_reset_key"),
    
    # ajax validation
    (r"^validate/$", "ajax_validation.views.validate", {"form_class": SignupForm}, "signup_form_validate"),
)
