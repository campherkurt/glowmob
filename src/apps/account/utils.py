from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.auth import login

from apps.account.signals import user_logged_in


LOGIN_REDIRECT_URLNAME = getattr(settings, "LOGIN_REDIRECT_URLNAME", "")


def get_default_redirect(request, redirect_field_name="next",
        login_redirect_urlname=LOGIN_REDIRECT_URLNAME, session_key_value="redirect_to"):
    """
    Returns the URL to be used in login procedures by looking at different
    values in the following order:
    
    - a REQUEST value, GET or POST, named "next" by default.
    - LOGIN_REDIRECT_URL - the URL in the setting
    - LOGIN_REDIRECT_URLNAME - the name of a URLconf entry in the settings
    """
    if login_redirect_urlname:
        default_redirect_to = reverse(login_redirect_urlname)
    else:
        default_redirect_to = settings.LOGIN_REDIRECT_URL
    redirect_to = request.REQUEST.get(redirect_field_name)
    if not redirect_to:
        # try the session if available
        if hasattr(request, "session"):
            redirect_to = request.session.get(session_key_value)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = default_redirect_to
    return redirect_to


def user_display(user):
    func = getattr(settings, "ACCOUNT_USER_DISPLAY", lambda user: user.username)
    return func(user)


def has_openid(request):
    """
    Given a HttpRequest determine whether the OpenID on it is associated thus
    allowing caller to know whether OpenID is good to depend on.
    """
    from django_openid.models import UserOpenidAssociation
    for association in UserOpenidAssociation.objects.filter(user=request.user):
        if association.openid == unicode(request.openid):
            return True
    return False


def perform_login(request, user):
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    login(request, user)