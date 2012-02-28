from django import forms
from apps.contact.models import Contact
from django.core.validators import email_re
from django.utils.translation import ugettext_lazy as _
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact

    def clean_contact(self):
        contact = self.cleaned_data["contact"]
        e = re.match(email_re, contact)
        m = re.match("[0-9]+", contact)

        if (m and contact == m.group() and len(m.group()) == 10) or (e and contact == e.group()):
            return self.cleaned_data["contact"]

        raise forms.ValidationError(_("Enter a valid email address or mobile number."))