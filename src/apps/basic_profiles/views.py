from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.basic_profiles.models import Profile
from apps.basic_profiles.forms import ProfileForm

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
from django.contrib import messages

def profiles(request, template_name="basic_profiles/profiles.html"):
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get("search", "")
    order = request.GET.get("order")
    if not order:
        order = "date"
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == "date":
        users = users.order_by("-date_joined")
    elif order == "name":
        users = users.order_by("username")
    return render_to_response(template_name, {
        "users":users,
        "order" : order,
        "search_terms" : search_terms
    }, context_instance=RequestContext(request))


def profile(request, username, template_name="basic_profiles/profile.html"):
    
    other_user = get_object_or_404(User, username=username)
    
    if request.user.is_authenticated():
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        is_me = False
    
    return render_to_response(template_name, {
        "is_me": is_me,
        "other_user": other_user,
    }, context_instance=RequestContext(request))


@login_required
def profile_edit(request, form_class=ProfileForm, **kwargs):
    
    template_name = kwargs.get("template_name", "basic_profiles/profile_edit.html")
    
    if request.is_ajax():
        template_name = kwargs.get(
            "template_name_facebox",
            "basic_profiles/profile_edit_facebox.html"
        )
    
    profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        profile_form = form_class(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.user.first_name = request.POST["first_name"];
            profile.user.last_name = request.POST["surname"];
            profile.user.email = request.POST["email"];
            
            profile.save()
            profile.user.save()

            messages.add_message(request, messages.SUCCESS, "Your profile has been updated.")
    else:
        profile_form = form_class(initial={'first_name': request.user.first_name, 'surname': request.user.last_name, 'email': request.user.email}, instance=profile)
    
    return render_to_response(template_name, {
        "profile": profile,
        "profile_form": profile_form,
    }, context_instance=RequestContext(request))

def toggle_images(request, status):
    if not request.user.is_anonymous():
        profile = request.user.profile_set.latest('pk')
        profile.display_mxit_images = True if 'on' == status else False
        profile.save()
    redirect_to = request.META.get('HTTP_REFERER', reverse('home'))
    return HttpResponseRedirect(redirect_to)