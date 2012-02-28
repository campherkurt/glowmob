from django import forms
from django.conf import settings

from apps.basic_profiles.models import Profile
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from django.contrib.auth.models import User
import re

REQUIRED_EMAIL = getattr(settings, "ACCOUNT_REQUIRED_EMAIL", False)
EMAIL_VERIFICATION = getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", False)
EMAIL_AUTHENTICATION = getattr(settings, "ACCOUNT_EMAIL_AUTHENTICATION", False)

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label = _("Name"),
        max_length = 255,
        required = False
    )

    surname = forms.CharField(
        label = _("Surname"),
        max_length = 255,
        required = False
    )

    email = forms.CharField(
        label = _("Email Address"),
        max_length = 255
    )

    years = []

    for i in range(date.today().year-40, date.today().year - 12):
        years.insert(0, i)
        
    birth_date = forms.DateField(label=_("* Date of Birth"), required=True, widget=SelectDateWidget(years=years))
    
    class Meta:
        model = Profile
        fields = ("first_name", "surname", "email", "mobile", "region", "city", "birth_date")
        #exclude = ["user", "name", "about", "location", "website"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if REQUIRED_EMAIL or EMAIL_VERIFICATION or EMAIL_AUTHENTICATION:
            self.fields["email"].label = ugettext("E-mail")
            self.fields["email"].required = True
        else:
            self.fields["email"].label = ugettext("E-mail (optional)")
            self.fields["email"].required = False

    def clean_mobile(self):
        if "mobile" in self.cleaned_data and len(self.cleaned_data["mobile"]) > 0:
            m = re.match("[0-9]+", self.cleaned_data["mobile"])

            if not m or self.cleaned_data["mobile"] != m.group() or len(m.group()) != 10:
                raise forms.ValidationError("Enter a valid mobile number")
        return self.cleaned_data["mobile"]

    def clean_email(self):
        if "email" in self.cleaned_data and len(self.cleaned_data["email"]) > 0:
            try:
                user = User.objects.get(email__iexact=self.cleaned_data["email"])
            except User.DoesNotExist:
                return self.cleaned_data["email"]

            if user != self.instance.user:
                raise forms.ValidationError("Email already exists")

        return self.cleaned_data["email"]