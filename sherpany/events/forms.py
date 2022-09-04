from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "start_at")

    def clean_start_at(self):
        start_at = self.cleaned_data.get("start_at")
        today = timezone.now().date()
        if start_at <= today:
            raise forms.ValidationError(_("Start at must greater than today."))

        return start_at
