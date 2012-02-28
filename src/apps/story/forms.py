from django import forms
from django.utils.translation import ugettext_lazy as _
from threadedcomments.models import ThreadedComment
from apps.story.models import CompetitionEntry, WriteStoryEntry, Review

SEARCH_BY = (
    (1, 'Title'),
    (2, 'Author'),
)

class SearchForm(forms.Form):
    search = forms.CharField(label="", max_length=255)
    search_by = forms.ChoiceField(label="", choices=SEARCH_BY)

class CommentForm(forms.ModelForm):
    class Meta:
        model = ThreadedComment
        exclude = ('content_type', 'object_id', 'parent', 'date_submitted', 'date_modified', 'date_approved', 'user', 'markup', 'is_public', 'is_approved', 'ip_address', 'status')

    def clean_comment(self):
        print len(self.cleaned_data["comment"])
        if len(self.cleaned_data["comment"].strip()) < 1:
            raise forms.ValidationError(_("Comment is required."))

        return self.cleaned_data["comment"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('content_type', 'object_id', 'user', 'is_approved')

    def clean_review(self):
        if len(self.cleaned_data["review"].strip()) < 1:
            raise forms.ValidationError(_("Review is required."))

        return self.cleaned_data["review"]

    def save(self, user, story, content_type):
        review = Review()
        review.user = user
        review.content_type = content_type
        review.object_id = story.id
        review.review = self.cleaned_data["review"]

        review.save()

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = CompetitionEntry
        exclude = ('user', 'competition')

    def clean_response(self):
        if len(self.cleaned_data["response"].strip()) < 1:
            raise forms.ValidationError(_("Response is required."))

        return self.cleaned_data["response"]

class WriteStoryEntryForm(forms.ModelForm):
    class Meta:
        model = WriteStoryEntry
    
    def clean(self):
        cleaned_data = self.cleaned_data
        if not (cleaned_data['cellphone'] or cleaned_data['email']):
            msg = _("You need to provide either your cellphone number or your email address.")
            self._errors["email"] = self.error_class([msg])
        if not cleaned_data['terms']:
            msg = _("You must agree to the terms before submitting your story.")
            self._errors["terms"] = self.error_class([msg])
        return cleaned_data