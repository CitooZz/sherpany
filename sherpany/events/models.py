from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class Event(models.Model):
    creator = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"))
    start_at = models.DateField(_("Start at"))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-start_at", "-id")

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.creator.email.split("@")[0]

    def is_owner(self, user) -> bool:
        """Check user is owner of event."""
        return self.creator == user

    def has_edit_permission(self, user) -> bool:
        """Check user has edit permission."""
        return self.is_owner(user)

    def is_participant(self, user) -> bool:
        """Check user is in participants"""
        return self.participants.filter(user=user).exists()

    def is_passed(self):
        today = timezone.now().date()
        return self.start_at <= today


class EventRSVP(models.Model):
    user = models.ForeignKey(User, related_name="rsvp", on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, related_name="participants", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [
            [
                "user",
                "event",
            ]
        ]

    def __str__(self):
        return f"{self.user.email}: {self.event.title}"
